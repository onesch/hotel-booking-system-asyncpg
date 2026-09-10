from redis.asyncio import Redis

from app.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
    ssl=False,
)
