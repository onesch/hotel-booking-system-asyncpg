from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.redis import redis
from app.settings import MAX_REQUESTS, WINDOW_SECONDS


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        current_count = await redis.incr(key)

        if current_count == 1:
            await redis.expire(key, WINDOW_SECONDS)

        if current_count > MAX_REQUESTS:
            ttl = await redis.ttl(key)

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too Many Requests",
                    "retry_after_seconds": ttl,
                },
            )
        return await call_next(request)
