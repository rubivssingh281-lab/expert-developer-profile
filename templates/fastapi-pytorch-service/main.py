from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.responses import JSONResponse
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

# --- Database & Unit of Work Setup ---
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

# --- Lifespan Context Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup Phase: Initialize ML weights and pre-warm GPU/CPU caches
    logger.info("server_startup_initiating")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeepInferenceModel().to(device)
    model.eval()

    # Model warm-up pass
    with torch.inference_mode():
        dummy_input = torch.randn(1, 10, device=device)
        _ = model(dummy_input)

    app.state.device = device
    app.state.model = model
    logger.info("server_startup_complete", device=str(device))
    yield
    # Shutdown Phase: Drain DB connection pools
    logger.info("server_shutdown_initiating")
    await engine.dispose()
    logger.info("server_shutdown_complete")

app = FastAPI(
    title="Production Async FastAPI + PyTorch Platform",
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

# --- Production Prediction Endpoint ---
@app.post(
    "/api/v1/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_201_CREATED,
)
async def predict_and_audit(
    request: Request,
    payload: PredictRequest,
    current_user: Annotated[AuthenticatedUser, Security(get_current_user, scopes=["inference:predict"])],
    db: DbSession,
) -> PredictResponse:
    # 1. Non-blocking inference on model loaded in app.state
    model: DeepInferenceModel = request.app.state.model
    device: torch.device = request.app.state.device

    def run_inference(raw_features: list[float]) -> tuple[int, float]:
        with torch.inference_mode():
            tensor_in = torch.tensor([raw_features], dtype=torch.float32, device=device)
            logits = model(tensor_in)
            probs = torch.softmax(logits, dim=-1)
            pred_class = int(torch.argmax(probs, dim=-1).item())
            confidence = float(probs[0, pred_class].item())
            return pred_class, confidence

    # Offload CPU/CUDA forward pass from the event loop
    predicted_class, confidence = await asyncio.to_thread(run_inference, payload.features)

    # 2. Persist audit log record bound by tenant_id (Enforcing Tenant Boundary)
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
    # Strict Object-Level Authorization Check (BOLA Mitigation)
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
