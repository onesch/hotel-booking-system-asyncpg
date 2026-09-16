from redis.asyncio import Redis

from app.settings import REDIS_URL

redis = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)
