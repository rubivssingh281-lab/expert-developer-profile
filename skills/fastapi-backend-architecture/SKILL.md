---
name: fastapi-backend-architecture
description: >-
  Use this skill when building, designing, or refactoring backend systems, FastAPI microservices, REST/GraphQL/gRPC APIs, asynchronous architectures, database schemas, PostgreSQL 18 performance tuning, SQLAlchemy 2.0 async, Redis caching, message queues, or applying Clean Architecture and Martin Fowler's Enterprise Application Architecture (PoEAA) patterns.
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

# --- Standardized Error Handling (RFC 7807 Problem Details) ---
class ProblemDetail(BaseModel):
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
    return JSONResponse(status_code=exc.status_code, content=problem.model_dump())

# --- Domain Schemas / DTOs (Pydantic v2) ---
class OrderCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    customer_id: UUID
    amount: float = Field(gt=0.0, description="Transaction amount must be positive")
    currency: str = Field(pattern="^[A-Z]{3}$", description="3-letter ISO currency code")

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
   - Regular `def` runs inside an external threadpool (default 40 threads in starlette). Use `async def` for I/O-bound tasks with async drivers; use `def` only if you must call synchronous blocking libraries.

---

## 4. PostgreSQL 18 Engineering Standards

### A. Indexing Strategies
- **B-Tree**: Primary keys, unique constraints, foreign keys, exact matches, and range queries (`<, <=, =, >=, >`).
- **GIN (Generalized Inverted Index)**: Essential for searching inside JSONB columns (`jsonb_path_ops`) and full-text search vectors (`tsvector`).
```sql
-- High-speed JSONB filtering index
CREATE INDEX idx_orders_metadata ON orders USING gin (metadata jsonb_path_ops);
```
- **BRIN (Block Range Index)**: Extremely compact indexes for massive append-only timeseries tables physically sorted by timestamp/ID.
- **Partial Indexes**: Index only active/frequent subsets to save disk and memory cache:
```sql
CREATE INDEX idx_active_tasks ON tasks (priority) WHERE status = 'PENDING';
```

### B. Query Performance & Concurrency
- **Analyze Query Plans**: Inspect execution plans using:
  `EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS) SELECT ...`
  Identify `Seq Scan` on large tables, nested loops on unindexed joins, or high buffer misses.
- **ACID Transaction Isolation Levels**:
  - `READ COMMITTED` (PostgreSQL default): Suitable for most queries; statements see data committed before the statement began.
  - `REPEATABLE READ`: Prevents non-repeatable reads and phantom reads; necessary for reporting batches or multi-query workflows.
  - `SERIALIZABLE`: Guarantees true serial execution; handles write skew; requires client retry logic upon serialization failure (`SQLSTATE 40001`).
- **Pessimistic vs Optimistic Locking**:
  - Pessimistic: `SELECT ... FOR UPDATE` (or `FOR UPDATE SKIP LOCKED` for background queue job consumers).
  - Optimistic: Maintain a `version_id` column; update with `WHERE id = :id AND version_id = :expected_version`.

---

## 5. Martin Fowler's Enterprise Application Architecture Patterns (PoEAA)

### A. Data Source & Domain Logic Patterns
1. **Unit of Work**:
   - Maintains a list of business objects affected by a business transaction and coordinates the writing out of changes and resolution of concurrency problems.
   - In SQLAlchemy async: The `AsyncSession` serves as the Unit of Work. Group cross-entity mutations within a single session transaction boundary.
2. **Repository / Data Mapper**:
   - Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects.
   - Isolates domain logic completely from database driver details, SQL dialect, or ORM quirks.
3. **Service Layer**:
   - Defines an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation.
   - Controllers in FastAPI should strictly call the Service Layer, never executing business rules or querying repositories directly.
4. **Data Transfer Object (DTO)**:
   - An object that carries data between processes to reduce the number of method calls and protect internal domain entities.
   - Pydantic v2 models represent DTOs: strictly separate external request/response schemas from database entity models.

### B. Enterprise Concurrency & State Patterns
1. **Optimistic Offline Lock**:
   - Prevents conflicts between concurrent business transactions by detecting a conflict and rolling back the transaction (e.g., version number check in update mutations).
2. **Pessimistic Offline Lock**:
   - Prevents conflicts between concurrent business transactions by allowing only one business transaction to access data at a time (e.g., exclusive lease records in distributed caches/databases).
3. **Value Object (VO)**:
   - Small immutable objects whose equality is based on value rather than identity (e.g., `Money(amount=100, currency="USD")`).
   - Implement via Python `dataclasses(frozen=True)` or Pydantic `frozen=True` models.
