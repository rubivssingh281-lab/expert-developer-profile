# PostgreSQL 18 Hybrid Retrieval, Transactional Outbox & ASGI Idempotency

Authoritative engineering manual on combining pgvector relaxed-order HNSW with BM25 full-text search via Reciprocal Rank Fusion, the Transactional Outbox pattern, and distributed ASGI idempotency middleware.

---

## 1. PostgreSQL 18 Hybrid Retrieval (`pgvector` HNSW + BM25 + RRF)

Modern RAG pipelines fuse dense vector semantic similarity with sparse lexical matching using Reciprocal Rank Fusion (RRF) inside a single SQL query:

```math
\text{RRF\_Score}(d) = \frac{w_{\text{vec}}}{k + \text{rank}_{\text{vec}}(d)} + \frac{w_{\text{lex}}}{k + \text{rank}_{\text{lex}}(d)}, \quad k = 60
```

### Production SQL Implementation with Mandatory BOLA Protection

```sql
WITH vector_search AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> :query_embedding) AS rank_vec
    FROM document_chunks
    WHERE tenant_id = :tenant_id
    ORDER BY embedding <=> :query_embedding
    LIMIT 50
),
text_search AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank_cd(text_tsv, plainto_tsquery('english', :query_text)) DESC) AS rank_lex
    FROM document_chunks
    WHERE tenant_id = :tenant_id AND text_tsv @@ plainto_tsquery('english', :query_text)
    LIMIT 50
)
SELECT
    COALESCE(v.id, t.id) AS document_id,
    COALESCE(1.0 / (60 + v.rank_vec), 0.0) + COALESCE(1.0 / (60 + t.rank_lex), 0.0) AS rrf_score
FROM vector_search v
FULL OUTER JOIN text_search t ON v.id = t.id
ORDER BY rrf_score DESC
LIMIT :limit_k;
```

---

## 2. Transactional Outbox Pattern with `SKIP LOCKED`

Prevents dual-write state corruption between PostgreSQL 18 and external message brokers (Kafka/RabbitMQ). Domain changes and event envelopes are written within the identical ACID transaction:

```sql
-- Inside application transaction:
INSERT INTO orders (id, tenant_id, total_amount, status) VALUES (:id, :tenant_id, :total, 'PENDING');
INSERT INTO outbox_events (id, aggregate_type, aggregate_id, event_type, payload)
VALUES (uuidv7(), 'Order', :id, 'OrderCreated', :payload_json);
COMMIT;
```

An asynchronous background worker selects events using `FOR UPDATE SKIP LOCKED`, dispatches to Kafka, and marks the event processed without lock contention.

---

## 3. Distributed ASGI Idempotency-Key Middleware

```python
from __future__ import annotations
import hashlib
from typing import Callable, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

class IdempotencyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, redis_client: Any) -> None:
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.method not in ("POST", "PUT", "PATCH"):
            return await call_next(request)

        key = request.headers.get("Idempotency-Key")
        if not key:
            return await call_next(request)

        body = await request.body()
        fingerprint = hashlib.sha256(body).hexdigest()
        redis_key = f"idempotency:{key}"

        acquired = await self.redis.set(redis_key, fingerprint, nx=True, ex=120)
        if not acquired:
            stored_fingerprint = await self.redis.get(redis_key)
            if stored_fingerprint != fingerprint:
                return JSONResponse(
                    status_code=422,
                    content={"type": "https://errors.example.com/idempotency-conflict", "title": "Payload fingerprint mismatch"},
                )
            return JSONResponse(
                status_code=409,
                content={"type": "https://errors.example.com/concurrent-request", "title": "Concurrent request in flight"},
            )

        return await call_next(request)
```

---

## 3. PostgreSQL 18 Native Hybrid Search Function & Async Outbox Worker

### 3.1 In-Database RRF Function
```sql
CREATE OR REPLACE FUNCTION hybrid_search(
    query_text TEXT,
    query_embedding vector(384),
    match_count INT DEFAULT 10,
    rrf_k INT DEFAULT 60
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    combined_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    WITH vector_search AS (
        SELECT d.id, ROW_NUMBER() OVER (ORDER BY d.embedding <=> query_embedding) AS rank
        FROM documents d
        ORDER BY d.embedding <=> query_embedding
        LIMIT match_count * 2
    ),
    fulltext_search AS (
        SELECT d.id, ROW_NUMBER() OVER (ORDER BY ts_rank_cd(d.search_vector, websearch_to_tsquery('english', query_text)) DESC) AS rank
        FROM documents d
        WHERE d.search_vector @@ websearch_to_tsquery('english', query_text)
        LIMIT match_count * 2
    )
    SELECT
        COALESCE(v.id, f.id) AS id,
        doc.title,
        doc.content,
        (COALESCE(1.0 / (rrf_k + v.rank), 0.0) + COALESCE(1.0 / (rrf_k + f.rank), 0.0))::FLOAT AS combined_score
    FROM vector_search v
    FULL OUTER JOIN fulltext_search f ON v.id = f.id
    JOIN documents doc ON doc.id = COALESCE(v.id, f.id)
    ORDER BY combined_score DESC
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
```

### 3.2 Asynchronous Outbox Worker Loop
```python
async def outbox_dispatcher_loop(session_factory: async_sessionmaker[AsyncSession]) -> None:
    """Polls and dispatches outbox events using PostgreSQL 18 SKIP LOCKED."""
    while True:
        async with session_factory() as session:
            async with session.begin():
                stmt = (
                    select(OutboxEvent)
                    .where(OutboxEvent.processed_at.is_(None))
                    .order_by(OutboxEvent.created_at.asc())
                    .limit(50)
                    .with_for_update(skip_locked=True)
                )
                events = (await session.scalars(stmt)).all()
                for event in events:
                    # Publish event payload to broker (Kafka / RabbitMQ)
                    event.processed_at = datetime.now(timezone.utc)
        await asyncio.sleep(1.0)
```

