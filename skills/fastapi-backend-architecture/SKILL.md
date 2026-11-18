---
name: fastapi-backend-architecture
description: >-
  Use this skill when building, designing, or refactoring backend systems, FastAPI microservices, REST/GraphQL/gRPC APIs, asynchronous architectures, database schemas, PostgreSQL 18 performance tuning, SQLAlchemy 2.0 async, Redis caching, message queues, or applying Clean Architecture and Martin Fowler's Enterprise Application Architecture (PoEAA) patterns.
trigger_patterns:
  keywords: ["fastapi", "asgi", "sqlalchemy", "asyncpg", "postgresql", "pgbouncer", "redis", "poeaa", "clean architecture", "pydantic", "unit of work", "repository pattern", "connection pool"]
  file_globs: ["**/*api*.py", "**/*router*.py", "**/*service*.py", "**/*repo*.py", "**/*model*.py", "**/*schema*.py", "**/alembic/**"]
  architectural_intents: ["rest-api-design", "database-optimization", "clean-architecture-refactoring", "connection-pool-sizing", "high-concurrency-backend", "concurrency-locking"]
theta_bindings:
  governing_parameters: ["sigma", "delta"]
  parameter_mappings:
    sigma:
      local-edge: "Single SQLite or Postgres asyncpg connection pool size <= 5, simple session handling"
      startup-1k-rps: "PostgreSQL asyncpg pool size 20, max_overflow 10, Redis caching for hot reads, keyset pagination"
      growth-10k-rps: "PgBouncer in transaction mode, read-write split replicas, Redis Lua atomic rate limiting, transactional outbox"
      hyperscale-100k-rps: "PostgreSQL 18 native AIO (io_uring), multi-region active-active read replicas, Kafka event-driven outbox, distributed Saga"
cross_skill_hooks:
  upstream:
    - skill: "agentic-orchestration"
      contract: "Receives structured tool invocation requests via JSON-RPC 2.0 / MCP schemas"
  downstream:
    - skill: "cybersecurity-appsec"
      contract: "Applies OAuth2 JWT scopes, Argon2id auth, BOLA object-level tenant queries, and RFC 9457 error details"
    - skill: "aiml-engineering"
      contract: "Dispatches requests to bounded asyncio.Queue dynamic micro-batching workers for non-blocking tensor inference"
    - skill: "devops-engineering"
      contract: "Exposes /healthz and /readyz probes, Prometheus metrics, and handles graceful SIGTERM lifespan shutdown"
lazy_references:
  - file: "references/fastapi-advanced-patterns.md"
    condition: "Activated when designing custom APIRoutes, dependency graphs, yield cleanups, SSE streaming, or RFC 9457 handlers"
  - file: "references/postgresql-18-internals.md"
    condition: "Activated when optimizing query plans, sizing PgBouncer pools, tuning autovacuum, or designing B-Tree/GIN/BRIN indexes"
  - file: "references/fowler-poeaa-complete-catalog.md"
    condition: "Activated when structuring Clean Architecture layers, Unit of Work, Data Mappers, Optimistic/Pessimistic Offline Locks"
  - file: "references/hybrid-pgvector-outbox-idempotency.md"
    condition: "Activated when implementing pgvector HNSW+BM25 RRF hybrid retrieval, Transactional Outbox, or ASGI idempotency middleware"
---

# FastAPI & Distributed Backend Architecture Skill

Authoritative knowledge base, production patterns, and database engineering guidelines synthesizing standards from:
- **FastAPI Official Tutorial & Advanced User Guide** — [FastAPI Advanced Production Patterns Reference](./references/fastapi-advanced-patterns.md)
- **PostgreSQL 18 Official Documentation Manual** — [PostgreSQL 18 Architecture & Internals Reference](./references/postgresql-18-internals.md)
- **Martin Fowler's Catalog of Enterprise Application Architecture (PoEAA)** — [Fowler's PoEAA Complete Architectural Catalog](./references/fowler-poeaa-complete-catalog.md)

---

## 1. Clean Architecture Standard

Maintain strict separation of concerns across service boundaries:
```text
app/
├── api/
│   └── v1/
│       ├── endpoints/      # HTTP route handlers (strictly request translation & response formatting)
│       └── router.py       # API router aggregation
├── core/
│   ├── config.py           # Pydantic v2 Settings (strictly validated environment configuration)
│   ├── security.py         # Password hashing (Argon2id), JWT generation/verification
│   └── database.py         # SQLAlchemy 2.0 AsyncEngine, async_sessionmaker
├── models/                 # SQLAlchemy 2.0 Declarative ORM domain entities
├── schemas/                # Pydantic v2 schemas / DTOs (strict Request and Response contracts)
├── repositories/           # Data access layer (pure SQL/ORM operations; no HTTP awareness)
├── services/               # Business logic domain layer (orchestrates repositories, external APIs)
└── main.py                 # FastAPI application instantiation, lifespan, middlewares, exception handlers
```

---

## 2. FastAPI Advanced Production Blueprint

### Lifespan, Database Pooling, and Dependency Injection
```python
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# --- Core Database Setup (PostgreSQL 18 + asyncpg) ---
DATABASE_URL = "postgresql+asyncpg://app_user:strong_password@localhost:5432/platform_db"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Test connection viability before handing to caller
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Warm connection pools, initialize telemetry, connect Redis
    yield
    # Shutdown: Gracefully drain connections and terminate pools
    await engine.dispose()

app = FastAPI(title="Production Platform API", version="1.0.0", lifespan=lifespan)

# --- Dependency Injection for DB Sessions ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

DbSession = Annotated[AsyncSession, Depends(get_db)]

# --- Standardized Error Handling (RFC 7807 / RFC 9457 Problem Details) ---
class ProblemDetail(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str | None = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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

# --- Domain Schemas / DTOs (Pydantic v2) ---
class OrderCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)
    customer_id: UUID
    amount: float = Field(gt=0.0, description="Transaction amount must be positive")
    currency: str = Field(pattern="^[A-Z]{3}$", description="3-letter ISO currency code")

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    id: UUID
    customer_id: UUID
    amount: float
    currency: str
    status: str
```

---

## 3. Async I/O Invariants
1. **Never Block the Event Loop**:
   - Calling `time.sleep()`, synchronous `requests.get()`, or unthreaded file I/O inside `async def` halts all concurrent requests.
   - Use `asyncio.sleep()`, `httpx.AsyncClient()`, or `aiofiles`.
   - If a library is strictly synchronous/blocking, offload it using `await asyncio.to_thread(sync_func, *args)`.
2. **Path Operations Execution Semantics**:
   - `async def` runs directly on the single-threaded asyncio event loop.
   - Regular `def` runs inside an external threadpool (default 40 threads in Starlette). Use `async def` for I/O-bound tasks with async drivers; use `def` only if you must call synchronous blocking libraries.

---

## 4. PostgreSQL 18 Engineering Standards & Capacity Math

### A. PgBouncer & PostgreSQL Sizing Math
To prevent CPU cache-thrashing and connection bloat:
$$\text{Postgres } \texttt{max_connections} = (\text{Total CPU Cores} \times 2) + \text{Reserved Buffer}$$
$$\text{Total DB Connections} = N_{\text{pods}} \times N_{\text{uvicorn\_workers}} \times (\text{pool\_size} + \text{max\_overflow}) \le 0.80 \times \text{max\_connections}_{\text{PgBouncer/PG}}$$

### B. Indexing Strategies
- **B-Tree**: Primary keys, unique constraints, foreign keys, exact matches, and range queries (`<, <=, =, >=, >`).
- **GIN (Generalized Inverted Index)**: Essential for searching inside JSONB columns (`jsonb_path_ops`) and full-text search vectors (`tsvector`).
- **BRIN (Block Range Index)**: Compact indexes for append-only timeseries tables physically sorted by timestamp/ID.
- **Partial Indexes**: Index only active/frequent subsets to save disk and memory cache.

---

## 5. Martin Fowler's Enterprise Application Architecture Patterns (PoEAA)
1. **Unit of Work**: Maintains a list of business objects affected by a business transaction (`AsyncSession`) and coordinates atomic commit/rollback.
2. **Repository / Data Mapper**: Mediates between domain logic and persistence using Python `Protocol` interfaces, isolating ORM details.
3. **Optimistic Offline Lock**: Uses a `version_id` column to prevent lost updates across long-lived user interactions.
4. **Pessimistic Offline Lock**: Uses `SELECT ... FOR UPDATE` (or `FOR UPDATE SKIP LOCKED` for task workers) to ensure single-actor mutation.
