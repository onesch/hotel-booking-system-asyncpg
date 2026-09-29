import httpx
import pytest

from app.settings import settings


@pytest.mark.asyncio
async def test_rate_limit_blocks_after_max_requests(
    run_server,
):
    url = f"http://127.0.0.1:8000/guests/"

    async with httpx.AsyncClient() as client:
        # Requests within the limit must be allowed.
        for _ in range(settings.max_requests):
            response = await client.get(url)

            assert response.status_code == 200

        # The next request must be blocked.
        response = await client.get(url)

    assert response.status_code == 429

    body = response.json()
    retry_after = int(response.headers["Retry-After"])

    assert body["detail"] == "Too Many Requests"
    assert retry_after == body["retry_after_seconds"]
    assert 0 < retry_after <= settings.window_seconds


@pytest.mark.asyncio
async def test_health_endpoint_is_not_rate_limited(
    run_server,
):
    health_url = f"http://127.0.0.1:8000/health"
    guests_url = f"http://127.0.0.1:8000/guests/"

    async with httpx.AsyncClient() as client:
        # Health requests must remain available beyond the normal limit.
        for _ in range(settings.max_requests + 1):
            response = await client.get(health_url)

            assert response.status_code == 200

        # Health requests must not consume the guests request limit.
        for _ in range(settings.max_requests):
            response = await client.get(guests_url)

            assert response.status_code == 200

        response = await client.get(guests_url)

    assert response.status_code == 429
