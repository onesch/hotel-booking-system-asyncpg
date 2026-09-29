import datetime
import pytest
from fastapi import HTTPException

from app.schemas.bookings import (
    BookingCreate,
    BookingDelete,
    BookingUpdate,
)

"""
Service -> correctly calls the Repository
        -> correctly handles the Repository result
"""


@pytest.mark.asyncio
async def test_create_booking(booking_service, booking_data):
    booking_service.repo.create.return_value = booking_data

    booking = BookingCreate(
        room_id=booking_data["room_id"],
        check_in_date=booking_data["check_in_date"],
        check_out_date=booking_data["check_out_date"],
    )

    result = await booking_service.create(
        booking,
        guest_id=booking_data["guest_id"],
    )

    assert result == booking_data

    booking_service.repo.create.assert_awaited_once_with(
        guest_id=booking_data["guest_id"],
        room_id=booking_data["room_id"],
        check_in_date=booking_data["check_in_date"],
        check_out_date=booking_data["check_out_date"],
    )


@pytest.mark.asyncio
async def test_get_booking_by_id(booking_service, booking_data):
    booking_service.repo.get_by_id.return_value = booking_data

    result = await booking_service.get_by_id(booking_data["id"])

    assert result == booking_data

    booking_service.repo.get_by_id.assert_awaited_once_with(
        booking_data["id"],
    )


@pytest.mark.asyncio
async def test_get_booking_by_id_not_found(booking_service):
    booking_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await booking_service.get_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Booking not found"

    booking_service.repo.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_bookings(booking_service, booking_data):
    booking_service.repo.get_all.return_value = [booking_data]

    result = await booking_service.get_all()

    assert result == [booking_data]

    booking_service.repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_booking(booking_service, booking_data):
    updated_booking = {
        **booking_data,
        "check_in_date": datetime.date(2026, 9, 1),
        "check_out_date": datetime.date(2026, 9, 5),
    }

    booking_service.repo.update.return_value = updated_booking

    booking = BookingUpdate(
        id=updated_booking["id"],
        check_in_date=updated_booking["check_in_date"],
        check_out_date=updated_booking["check_out_date"],
    )

    result = await booking_service.update(booking)

    assert result == updated_booking

    booking_service.repo.update.assert_awaited_once_with(
        id=updated_booking["id"],
        check_in_date=updated_booking["check_in_date"],
        check_out_date=updated_booking["check_out_date"],
    )


@pytest.mark.asyncio
async def test_update_booking_not_found(booking_service):
    booking_service.repo.update.return_value = None

    booking = BookingUpdate(
        id=999,
        check_in_date=datetime.date(2026, 9, 1),
        check_out_date=datetime.date(2026, 9, 5),
    )

    with pytest.raises(HTTPException) as exc:
        await booking_service.update(booking)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Booking not found"

    booking_service.repo.update.assert_awaited_once_with(
        id=999,
        check_in_date=datetime.date(2026, 9, 1),
        check_out_date=datetime.date(2026, 9, 5),
    )


@pytest.mark.asyncio
async def test_delete_booking(booking_service, booking_data):
    booking_service.repo.delete.return_value = booking_data

    booking = BookingDelete(id=booking_data["id"])

    result = await booking_service.delete(booking)

    assert result == booking_data

    booking_service.repo.delete.assert_awaited_once_with(
        id=booking_data["id"],
    )


@pytest.mark.asyncio
async def test_delete_booking_not_found(booking_service):
    booking_service.repo.delete.return_value = None

    booking = BookingDelete(id=999)

    with pytest.raises(HTTPException) as exc:
        await booking_service.delete(booking)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Booking not found"

    booking_service.repo.delete.assert_awaited_once_with(id=999)
