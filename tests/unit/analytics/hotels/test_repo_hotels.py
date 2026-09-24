import pytest


@pytest.mark.asyncio
async def test_room_type_counts(
    hotel_analytics_repository,
    room_type_count_data,
):
    hotel_analytics_repository.db.fetch.return_value = [room_type_count_data]

    result = await hotel_analytics_repository.room_type_counts(1)

    assert result == [room_type_count_data]
    query, *args = hotel_analytics_repository.db.fetch.call_args.args
    assert "COUNT(r.id) AS room_count" in query
    assert "WHERE r.hotel_id = $1" in query
    assert "GROUP BY" in query
    assert args == [1]


@pytest.mark.asyncio
async def test_monthly_bookings(
    hotel_analytics_repository,
    monthly_bookings_data,
):
    hotel_analytics_repository.db.fetch.return_value = [monthly_bookings_data]

    result = await hotel_analytics_repository.monthly_bookings(1)

    assert result == [monthly_bookings_data]
    query, *args = hotel_analytics_repository.db.fetch.call_args.args
    assert "DATE_TRUNC('month', b.check_in_date) AS month" in query
    assert "INNER JOIN rooms AS r" in query
    assert "WHERE r.hotel_id = $1" in query
    assert "GROUP BY DATE_TRUNC('month', b.check_in_date)" in query
    assert args == [1]


@pytest.mark.asyncio
async def test_room_type_popularity(
    hotel_analytics_repository,
    room_type_popularity_data,
):
    hotel_analytics_repository.db.fetch.return_value = [
        room_type_popularity_data
    ]

    result = await hotel_analytics_repository.room_type_popularity(1)

    assert result == [room_type_popularity_data]
    query, *args = hotel_analytics_repository.db.fetch.call_args.args
    assert "COUNT(b.id) AS booking_count" in query
    assert "WHERE r.hotel_id = $1" in query
    assert "ROW_NUMBER() OVER" in query
    assert "ORDER BY booking_count DESC, room_type_id" in query
    assert args == [1]
