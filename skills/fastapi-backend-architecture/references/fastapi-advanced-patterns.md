# FastAPI Advanced Production Patterns Reference

Synthesized from **FastAPI Official Tutorial & Advanced User Guide**.

---

## 1. Custom APIRoute Class for Latency & Error Logging
Rather than using bulky middleware that wraps every request, use custom `APIRoute` to access raw route signatures, calculate execution duration, and catch route-level exceptions:

```python
import time
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
import structlog

logger = structlog.get_logger()

class TimedLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start_time = time.perf_counter()
            try:
                response: Response = await original_route_handler(request)
                duration = time.perf_counter() - start_time
                response.headers["X-Process-Time"] = f"{duration:.4f}s"
                logger.info("api_request_success", path=request.url.path, duration=duration)
                return response
            except Exception as exc:
                duration = time.perf_counter() - start_time
                logger.error("api_request_failed", path=request.url.path, duration=duration, error=str(exc))
                raise exc

        return custom_route_handler
```

Attached to router:
```python
router = APIRouter(route_class=TimedLoggingRoute)
```

### B. Custom Request Subclassing (`GzipRequest` & `GzipRoute`)
An alternative to global middleware for transparently decompressing request bodies:

```python
import gzip
from collections.abc import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)
        return custom_route_handler
```

---

## 2. Advanced Dependency Injection, OAuth2 Scopes & Yield Dependencies

### A. Fine-Grained Authorization via `SecurityScopes`
Configure granular permission scopes (e.g., `read:users`, `write:orders`) directly in route handlers and dependency resolvers:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes={
        "read:orders": "Read permission for order entities",
        "write:orders": "Mutation permission for order entities",
        "admin": "Full system administrative access",
    },
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    # Authenticate token and extract assigned scopes
    token_data = decode_jwt(token)
    for required_scope in security_scopes.scopes:
        if required_scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission scope: {required_scope}",
            )
    return token_data.user

# Route demanding specific security scope
@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
async def create_order(
    current_user: Annotated[User, Security(get_current_user, scopes=["write:orders"])]
):
    ...
```

### B. Yield Dependencies with Redis Connection Pools
Dependencies can yield resources, clean up after the request finishes, and depend on other dependencies hierarchically:

```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends, Header, HTTPException, status
from redis.asyncio import Redis, ConnectionPool

redis_pool = ConnectionPool.from_url("redis://localhost:6379/0", max_connections=20)

async def get_redis_client() -> AsyncGenerator[Redis, None]:
    client = Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.aclose()

async def verify_rate_limit(
    x_api_key: Annotated[str, Header()],
    redis: Annotated[Redis, Depends(get_redis_client)],
):
    key = f"rate_limit:{x_api_key}"
    current_count = await redis.incr(key)
    if current_count == 1:
        await redis.expire(key, 60)
    if current_count > 100:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
```

---

## 3. Streaming Responses & Server-Sent Events (SSE)
Stream large outputs or real-time LLM token streams efficiently without blocking:

```python
import asyncio
from typing import AsyncGenerator
from fastapi.responses import StreamingResponse

async def token_generator() -> AsyncGenerator[str, None]:
    for word in ["Synthesizing", "enterprise", "architecture", "patterns..."]:
        await asyncio.sleep(0.05)
        yield f"data: {word}\n\n"

@app.get("/api/v1/stream")
async def stream_tokens():
    return StreamingResponse(token_generator(), media_type="text/event-stream")
```

---

## 4. RFC 7807 Structured Problem Details
Never emit ad-hoc error JSON. Always return RFC 7807 standard objects:

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Your current balance is $20.00, but the transaction requested $50.00.",
  "instance": "/api/v1/accounts/123/withdraw"
}
```
