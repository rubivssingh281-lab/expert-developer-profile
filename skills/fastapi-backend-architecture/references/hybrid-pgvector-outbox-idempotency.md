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
