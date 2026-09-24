import pytest
from fastapi import HTTPException


@pytest.mark.parametrize(
    ("method_name", "result_fixture"),
    [
        ("room_type_counts", "room_type_count_data"),
        ("monthly_bookings", "monthly_bookings_data"),
        ("room_type_popularity", "room_type_popularity_data"),
    ],
)
@pytest.mark.asyncio
async def test_hotel_analytics(
    hotel_analytics_service,
    hotel_data,
    method_name,
    result_fixture,
    request,
):
    analytics_data = request.getfixturevalue(result_fixture)
    hotel_analytics_service.hotel_repo.get_by_id.return_value = hotel_data
    repository_method = getattr(
        hotel_analytics_service.analytics_repo,
        method_name,
    )
    repository_method.return_value = [analytics_data]

    result = await getattr(hotel_analytics_service, method_name)(
        hotel_data["id"]
    )

    assert result == [analytics_data]
    hotel_analytics_service.hotel_repo.get_by_id.assert_awaited_once_with(
        hotel_data["id"]
    )
    repository_method.assert_awaited_once_with(hotel_data["id"])


@pytest.mark.parametrize(
    "method_name",
    [
        "room_type_counts",
        "monthly_bookings",
        "room_type_popularity",
    ],
)
@pytest.mark.asyncio
async def test_hotel_analytics_hotel_not_found(
    hotel_analytics_service,
    method_name,
):
    hotel_analytics_service.hotel_repo.get_by_id.return_value = None
    repository_method = getattr(
        hotel_analytics_service.analytics_repo,
        method_name,
    )

    with pytest.raises(HTTPException) as exc:
        await getattr(hotel_analytics_service, method_name)(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel not found"
    hotel_analytics_service.hotel_repo.get_by_id.assert_awaited_once_with(999)
    repository_method.assert_not_awaited()
