from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.redis import redis
from app.settings import settings


RATE_LIMIT_SCRIPT = """
local current_count = redis.call("INCR", KEYS[1])

if current_count == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

return current_count
"""


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Limit the number of requests from each client IP."""

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks.
        if request.url.path == "/health":
            return await call_next(request)

        # Build a Redis key for the current client.
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        # Atomically increment the request counter
        # and set expiration for a new key.
        current_count = await redis.eval(
            RATE_LIMIT_SCRIPT,
            1,
            key,
            settings.window_seconds,
        )

        # Block requests that exceed the configured limit.
        if current_count > settings.max_requests:
            ttl = await redis.ttl(key)

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too Many Requests",
                    "retry_after_seconds": ttl,
                },
                headers={
                    "Retry-After": str(ttl),
                },
            )

        # Continue processing requests within the limit.
        return await call_next(request)
