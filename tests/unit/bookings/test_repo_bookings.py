import pytest
import asyncpg
from fastapi import HTTPException

"""
Repository -> raw SQL queries -> PostgreSQL
"""


@pytest.mark.asyncio
async def test_create_booking(booking_repository, booking_data):
    booking_repository.db.fetchrow.return_value = booking_data

    result = await booking_repository.create(
        guest_id=booking_data["guest_id"],
        room_id=booking_data["room_id"],
        check_in_date=booking_data["check_in_date"],
        check_out_date=booking_data["check_out_date"],
    )

    assert result == booking_data

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "INSERT INTO bookings" in query
    assert "VALUES ($1, $2, $3, $4)" in query
    assert "RETURNING *" in query

    assert args == [
        booking_data["guest_id"],
        booking_data["room_id"],
        booking_data["check_in_date"],
        booking_data["check_out_date"],
    ]


@pytest.mark.asyncio
async def test_create_booking_conflict(
    booking_repository,
    booking_data,
):
    booking_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.ExclusionViolationError()
    )

    with pytest.raises(HTTPException) as exc:
        await booking_repository.create(
            guest_id=booking_data["guest_id"],
            room_id=booking_data["room_id"],
            check_in_date=booking_data["check_in_date"],
            check_out_date=booking_data["check_out_date"],
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Room is already booked for these dates"
    )


@pytest.mark.asyncio
async def test_get_booking_by_id(
    booking_repository,
    booking_data,
):
    booking_repository.db.fetchrow.return_value = booking_data

    result = await booking_repository.get_by_id(
        booking_data["id"]
    )

    assert result == booking_data

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM bookings" in query
    assert "WHERE id = $1" in query

    assert args == [booking_data["id"]]


@pytest.mark.asyncio
async def test_get_booking_by_id_not_found(
    booking_repository,
):
    booking_repository.db.fetchrow.return_value = None

    result = await booking_repository.get_by_id(999)

    assert result is None

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM bookings" in query
    assert "WHERE id = $1" in query

    assert args == [999]


@pytest.mark.asyncio
async def test_get_all_bookings(
    booking_repository,
    booking_data,
):
    booking_repository.db.fetch.return_value = [booking_data]

    result = await booking_repository.get_all()

    assert result == [booking_data]

    booking_repository.db.fetch.assert_awaited_once()

    query = booking_repository.db.fetch.call_args.args[0]

    assert "SELECT" in query
    assert "FROM bookings" in query
    assert "ORDER BY id" in query


@pytest.mark.asyncio
async def test_update_booking(
    booking_repository,
    booking_data,
):
    updated_booking = {
        **booking_data,
        "check_in_date": "2026-10-15",
        "check_out_date": "2026-10-20",
    }

    booking_repository.db.fetchrow.return_value = updated_booking

    result = await booking_repository.update(
        id=booking_data["id"],
        check_in_date=updated_booking["check_in_date"],
        check_out_date=updated_booking["check_out_date"],
    )

    assert result == updated_booking

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "UPDATE bookings" in query
    assert "SET" in query
    assert "check_in_date = $2" in query
    assert "check_out_date = $3" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [
        booking_data["id"],
        updated_booking["check_in_date"],
        updated_booking["check_out_date"],
    ]


@pytest.mark.asyncio
async def test_update_booking_not_found(
    booking_repository,
):
    booking_repository.db.fetchrow.return_value = None

    result = await booking_repository.update(
        id=999,
        check_in_date="2026-10-15",
        check_out_date="2026-10-20",
    )

    assert result is None

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "UPDATE bookings" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [
        999,
        "2026-10-15",
        "2026-10-20",
    ]


@pytest.mark.asyncio
async def test_update_booking_conflict(
    booking_repository,
    booking_data,
):
    booking_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.ExclusionViolationError()
    )

    with pytest.raises(HTTPException) as exc:
        await booking_repository.update(
            id=booking_data["id"],
            check_in_date="2026-10-15",
            check_out_date="2026-10-20",
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Room is already booked for these dates"
    )


@pytest.mark.asyncio
async def test_delete_booking(
    booking_repository,
    booking_data,
):
    booking_repository.db.fetchrow.return_value = booking_data

    result = await booking_repository.delete(
        id=booking_data["id"]
    )

    assert result == booking_data

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "DELETE FROM bookings" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [booking_data["id"]]


@pytest.mark.asyncio
async def test_delete_booking_not_found(
    booking_repository,
):
    booking_repository.db.fetchrow.return_value = None

    result = await booking_repository.delete(id=999)

    assert result is None

    booking_repository.db.fetchrow.assert_awaited_once()

    query, *args = booking_repository.db.fetchrow.call_args.args

    assert "DELETE FROM bookings" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [999]
