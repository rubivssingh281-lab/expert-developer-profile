from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import time
from typing import Annotated, AsyncGenerator
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Response, Security, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import structlog
import torch
import torch.nn as nn

# --- Structured Logging Configuration ---
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# --- Security & Cryptography Configuration ---
JWT_SECRET_KEY = "CHANGE_IN_PRODUCTION_TO_SECURE_ASYMMETRIC_OR_VAULT_KEY"
JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes={
        "inference:predict": "Permission to run machine learning model inference",
        "records:read": "Permission to inspect persisted prediction audit logs",
        "admin": "Full system administrative control",
    },
)

# --- Database & Unit of Work Setup (PostgreSQL 18 + asyncpg) ---
DATABASE_URL = "postgresql+asyncpg://app_user:strong_password@localhost:5432/platform_db"
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_recycle=1800,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(index=True, nullable=False)
    input_features: Mapped[list[float]] = mapped_column(nullable=False)
    prediction_score: Mapped[float] = mapped_column(nullable=False)
    predicted_class: Mapped[int] = mapped_column(nullable=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error("database_transaction_aborted", error=str(exc))
            raise

DbSession = Annotated[AsyncSession, Depends(get_db)]

# --- Neural Network Model Architecture ---
class DeepInferenceModel(nn.Module):
    def __init__(self, input_dim: int = 10, hidden_dim: int = 64, num_classes: int = 2) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

# --- Dynamic Micro-Batching Configuration & Types ---
BATCH_SIZE = 16
BATCH_TIMEOUT_SECONDS = 0.015  # 15ms collection window to protect P99 latency
MAX_QUEUE_CAPACITY = 1024

class QueueItem:
    __slots__ = ("features", "future", "created_at")

    def __init__(self, features: list[float], future: asyncio.Future[tuple[int, float]]) -> None:
        self.features = features
        self.future = future
        self.created_at = time.perf_counter()

# Global Bounded Batching Queue
inference_queue: asyncio.Queue[QueueItem] = asyncio.Queue(maxsize=MAX_QUEUE_CAPACITY)

# Telemetry counters
TOTAL_REQUESTS = 0
TOTAL_BATCHES = 0

async def dynamic_batch_worker(app: FastAPI) -> None:
    """Continuous background worker collecting dynamic micro-batches for PyTorch inference."""
    device: torch.device = app.state.device
    model: DeepInferenceModel = app.state.model
    global TOTAL_BATCHES

    while True:
        batch: list[QueueItem] = []
        try:
            # Block until first item arrives
            first_item = await inference_queue.get()
            batch.append(first_item)
        except asyncio.CancelledError:
            break

        # Accumulate up to BATCH_SIZE within timeout
        start_time = time.perf_counter()
        while len(batch) < BATCH_SIZE:
            elapsed = time.perf_counter() - start_time
            remaining = BATCH_TIMEOUT_SECONDS - elapsed
            if remaining <= 0:
                break
            try:
                item = await asyncio.wait_for(inference_queue.get(), timeout=remaining)
                batch.append(item)
            except asyncio.TimeoutError:
                break

        TOTAL_BATCHES += 1
        tensor_inputs = [item.features for item in batch]
        futures = [item.future for item in batch]

        try:
            # Execute vectorized forward pass with CUDA OOM recovery
            def execute_forward() -> list[tuple[int, float]]:
                with torch.inference_mode():
                    tensor_batch = torch.tensor(tensor_inputs, dtype=torch.float32, device=device)
                    logits = model(tensor_batch)
                    probs = torch.softmax(logits, dim=-1)
                    classes = torch.argmax(probs, dim=-1).cpu().tolist()
                    confidences = [float(probs[i, c].item()) for i, c in enumerate(classes)]
                    return list(zip(classes, confidences))

            try:
                results = await asyncio.to_thread(execute_forward)
            except torch.cuda.OutOfMemoryError as oom_exc:
                logger.error("cuda_oom_detected_clearing_cache", error=str(oom_exc))
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                raise oom_exc

            for future, res in zip(futures, results):
                if not future.done():
                    future.set_result(res)

        except Exception as exc:
            for future in futures:
                if not future.done():
                    future.set_exception(exc)
        finally:
            for _ in range(len(batch)):
                inference_queue.task_done()

# --- Lifespan Context Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("server_startup_initiating")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeepInferenceModel().to(device)
    model.eval()

    # Pre-warming pass
    with torch.inference_mode():
        dummy_input = torch.randn(1, 10, device=device)
        _ = model(dummy_input)

    app.state.device = device
    app.state.model = model
    app.state.is_ready = True

    # Spawn dynamic micro-batch worker task
    worker_task = asyncio.create_task(dynamic_batch_worker(app))
    logger.info("server_startup_complete", device=str(device))

    yield

    # Shutdown Phase
    logger.info("server_shutdown_initiating")
    app.state.is_ready = False
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass
    await engine.dispose()
    logger.info("server_shutdown_complete")

app = FastAPI(
    title="Production Async FastAPI + PyTorch Platform (v2.0 4-Skill Composition)",
    version="2.0.0",
    lifespan=lifespan,
)

# --- Standardized RFC 9457 Error Response ---
class ProblemDetail(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str | None = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    problem = ProblemDetail(
        title="HTTP Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=str(request.url.path),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )

# --- AuthN / AuthZ Token Verification ---
class AuthenticatedUser(BaseModel):
    user_id: UUID
    tenant_id: UUID
    scopes: list[str]

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AuthenticatedUser:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_scopes: list[str] = payload.get("scopes", [])
        for scope in security_scopes.scopes:
            if scope not in user_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission scope: {scope}",
                )
        return AuthenticatedUser(
            user_id=UUID(payload["sub"]),
            tenant_id=UUID(payload["tenant_id"]),
            scopes=user_scopes,
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

# --- Strict Pydantic v2 DTOs ---
class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    features: list[float] = Field(min_length=10, max_length=10, description="10-dimensional input vector")

class PredictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    record_id: UUID
    predicted_class: int
    confidence: float

# --- Observability & Health Endpoints (DevOps Engineering Contract) ---
@app.get("/healthz", response_class=PlainTextResponse)
@app.get("/health/live")
async def liveness_probe() -> dict[str, str] | str:
    return {"status": "healthy"}

@app.get("/readyz", response_class=PlainTextResponse)
@app.get("/health/ready")
async def readiness_probe(request: Request) -> Response:
    is_ready = getattr(request.app.state, "is_ready", False)
    if is_ready and inference_queue.qsize() < MAX_QUEUE_CAPACITY:
        return JSONResponse({"status": "ready"}, status_code=status.HTTP_200_OK)
    return JSONResponse({"status": "not_ready"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

@app.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics() -> str:
    return (
        f"# HELP inference_requests_total Total number of inference requests\n"
        f"# TYPE inference_requests_total counter\n"
        f"inference_requests_total {TOTAL_REQUESTS}\n"
        f"# HELP inference_batches_total Total micro-batches processed\n"
        f"# TYPE inference_batches_total counter\n"
        f"inference_batches_total {TOTAL_BATCHES}\n"
        f"# HELP inference_queue_depth Current depth of inference queue\n"
        f"# TYPE inference_queue_depth gauge\n"
        f"inference_queue_depth {inference_queue.qsize()}\n"
    )

# --- Production Prediction Endpoint (4-Skill Contract) ---
@app.post(
    "/api/v1/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_201_CREATED,
)
async def predict_and_audit(
    payload: PredictRequest,
    current_user: Annotated[AuthenticatedUser, Security(get_current_user, scopes=["inference:predict"])],
    db: DbSession,
) -> PredictResponse:
    global TOTAL_REQUESTS
    TOTAL_REQUESTS += 1

    # Guard against queue saturation (backpressure / load shedding)
    if inference_queue.qsize() >= MAX_QUEUE_CAPACITY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inference queue saturated; load shedding active",
        )

    # 1. Enqueue payload for dynamic micro-batching
    loop = asyncio.get_running_loop()
    future: asyncio.Future[tuple[int, float]] = loop.create_future()
    item = QueueItem(features=payload.features, future=future)
    await inference_queue.put(item)

    # 2. Await batch resolution with overall request timeout
    try:
        async with asyncio.timeout(3.0):
            predicted_class, confidence = await future
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Inference execution timed out",
        )

    # 3. Persist audit log record bound by tenant_id (Enforcing Tenant Boundary)
    record = PredictionRecord(
        tenant_id=current_user.tenant_id,
        input_features=payload.features,
        prediction_score=confidence,
        predicted_class=predicted_class,
    )
    db.add(record)
    await db.flush()

    logger.info(
        "inference_completed",
        tenant_id=str(current_user.tenant_id),
        record_id=str(record.id),
        predicted_class=predicted_class,
        confidence=confidence,
    )

    return PredictResponse(
        record_id=record.id,
        predicted_class=predicted_class,
        confidence=confidence,
    )

# --- BOLA-Protected Record Query Endpoint ---
@app.get(
    "/api/v1/records/{record_id}",
    response_model=PredictResponse,
)
async def get_prediction_record(
    record_id: UUID,
    current_user: Annotated[AuthenticatedUser, Security(get_current_user, scopes=["records:read"])],
    db: DbSession,
) -> PredictResponse:
    query = select(PredictionRecord).where(
        PredictionRecord.id == record_id,
        PredictionRecord.tenant_id == current_user.tenant_id,  # Hard boundary enforcement
    )
    record = await db.scalar(query)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return PredictResponse(
        record_id=record.id,
        predicted_class=record.predicted_class,
        confidence=record.prediction_score,
    )
