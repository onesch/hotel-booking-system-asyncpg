import pytest_asyncio
from redis.asyncio import Redis

from app.settings import TEST_REDIS_URL


@pytest_asyncio.fixture(autouse=True)
async def test_redis(monkeypatch):
    test_redis_client = Redis.from_url(
        TEST_REDIS_URL,
        decode_responses=True,
    )

    await test_redis_client.flushdb()

    monkeypatch.setattr(
        "app.middlewares.redis",
        test_redis_client,
    )

    try:
        yield test_redis_client
    finally:
        await test_redis_client.flushdb()
        await test_redis_client.aclose()
