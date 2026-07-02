"""
Cross-cutting HTTP middleware for request IDs, access logs, and simple
single-process rate limiting.
"""
import logging
import time
import uuid
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import settings

logger = logging.getLogger("lenspilot")

# client_key -> recent request timestamps
_hits: dict[str, deque[float]] = defaultdict(deque)


def _bearer_token(request: Request) -> str | None:
    authorization = request.headers.get("authorization")
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return None


def _client_key(request: Request) -> str:
    """Rate-limit by API key when supplied; otherwise fall back to client IP."""
    api_key = request.headers.get("x-api-key") or _bearer_token(request)
    if api_key:
        return f"key:{api_key}"

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return f"ip:{forwarded_for.split(',')[0].strip()}"

    client = request.client.host if request.client else "unknown"
    return f"ip:{client}"


def _is_rate_limited(key: str) -> bool:
    limit = settings.RATE_LIMIT_PER_MINUTE
    if limit <= 0:
        return False

    now = time.time()
    window_start = now - 60
    hits = _hits[key]

    while hits and hits[0] < window_start:
        hits.popleft()

    if len(hits) >= limit:
        return True

    hits.append(now)
    return False


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Adds `x-request-id`, logs request timing, and limits expensive endpoints.

    The limiter is intentionally simple and in-memory for the MVP. If the
    backend scales to multiple replicas, replace `_hits` with Redis or another
    shared store.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        start = time.time()

        rate_limited_paths = {
            "/chat",
            "/ingest",
            f"{settings.API_PREFIX}/chat",
            f"{settings.API_PREFIX}/ingest",
        }

        if request.url.path in rate_limited_paths:
            key = _client_key(request)
            if _is_rate_limited(key):
                logger.warning("[%s] rate limited: %s", request_id, key)
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Too many requests. Please slow down and try again shortly."
                    },
                    headers={"x-request-id": request_id},
                )

        response = await call_next(request)
        response.headers["x-request-id"] = request_id

        duration_ms = (time.time() - start) * 1000
        logger.info(
            "[%s] %s %s -> %s (%.1fms)",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
