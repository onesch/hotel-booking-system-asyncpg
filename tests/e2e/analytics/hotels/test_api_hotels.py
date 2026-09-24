import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.parametrize(
    ("path", "method_name", "result_fixture"),
    [
        ("room-types/count", "room_type_counts", "room_type_count_data"),
        ("bookings/monthly", "monthly_bookings", "monthly_bookings_data"),
        ("room-types/popularity", "room_type_popularity", "room_type_popularity_data"),
    ],
)
@pytest.mark.asyncio
async def test_get_hotel_analytics(
    api_hotel_analytics_service,
    hotel_data,
    path,
    method_name,
    result_fixture,
    request,
    monkeypatch,
):
    analytics_data = request.getfixturevalue(result_fixture)
    service_method = getattr(api_hotel_analytics_service, method_name)
    service_method.return_value = [analytics_data]
    monkeypatch.setattr(
        "app.routers.analytics.hotels.hotel_analytics_service",
        api_hotel_analytics_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get(
            f"/hotel-analytics/{hotel_data['id']}/{path}"
        )

    expected = dict(analytics_data)
    if method_name == "monthly_bookings":
        expected["month"] = analytics_data["month"].isoformat()

    assert response.status_code == 200
    assert response.json() == [expected]
    service_method.assert_awaited_once_with(hotel_data["id"])


@pytest.mark.parametrize(
    ("path", "method_name"),
    [
        ("room-types/count", "room_type_counts"),
        ("bookings/monthly", "monthly_bookings"),
        ("room-types/popularity", "room_type_popularity"),
    ],
)
@pytest.mark.asyncio
async def test_get_hotel_analytics_hotel_not_found(
    api_hotel_analytics_service,
    path,
    method_name,
    monkeypatch,
):
    service_method = getattr(api_hotel_analytics_service, method_name)
    service_method.side_effect = HTTPException(
        status_code=404,
        detail="Hotel not found",
    )
    monkeypatch.setattr(
        "app.routers.analytics.hotels.hotel_analytics_service",
        api_hotel_analytics_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get(f"/hotel-analytics/999/{path}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Hotel not found"}
    service_method.assert_awaited_once_with(999)
