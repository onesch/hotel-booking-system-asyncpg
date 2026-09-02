from datetime import date
import asyncpg
import pytest
from fastapi import HTTPException


# ------------ CHECK ------------

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (date(2026, 10, 5), date(2026, 10, 10)),
        (date(2026, 10, 10), date(2026, 10, 15)),
        (date(2026, 10, 15), date(2026, 10, 20)),
    ],
)
async def test_booking_valid_dates(
    booking_repository,
    clean_database,
    guest,
    room,
    check_in,
    check_out,
):
    result = await booking_repository.create(
        guest_id=guest["id"],
        room_id=room["id"],
        check_in_date=check_in,
        check_out_date=check_out,
    )

    assert result is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (date(2026, 10, 10), date(2026, 10, 10)),  # same dates
        (date(2026, 10, 15), date(2026, 10, 10)),  # checkout before checkin
    ],
)
async def test_booking_invalid_dates(
    booking_repository,
    clean_database,
    guest,
    room,
    check_in,
    check_out,
):
    with pytest.raises(Exception):
        await booking_repository.create(
            guest_id=guest["id"],
            room_id=room["id"],
            check_in_date=check_in,
            check_out_date=check_out,
        )


# ----------- EXCLUDE -----------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (date(2026, 10, 12), date(2026, 10, 18)),  # overlap inside
        (date(2026, 10, 3), date(2026, 10, 18)),  # starts before
        (date(2026, 10, 11), date(2026, 10, 14)),  # fully inside
    ],
)
async def test_booking_overlap_conflict(
    booking_repository,
    clean_database,
    guest,
    second_guest,
    room,
    check_in,
    check_out,
):
    await booking_repository.create(
        guest_id=guest["id"],
        room_id=room["id"],
        check_in_date=date(2026, 10, 10),
        check_out_date=date(2026, 10, 15),
    )

    with pytest.raises(HTTPException) as exc:
        await booking_repository.create(
            guest_id=second_guest["id"],
            room_id=room["id"],
            check_in_date=check_in,
            check_out_date=check_out,
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Room is already booked for these dates"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (date(2026, 10, 15), date(2026, 10, 20)),  # starts at checkout
        (date(2026, 10, 5), date(2026, 10, 10)),  # ends at check-in
    ],
)
async def test_booking_no_overlap(
    booking_repository,
    clean_database,
    guest,
    second_guest,
    room,
    check_in,
    check_out,
):
    await booking_repository.create(
        guest_id=guest["id"],
        room_id=room["id"],
        check_in_date=date(2026, 10, 10),
        check_out_date=date(2026, 10, 15),
    )

    result = await booking_repository.create(
        guest_id=second_guest["id"],
        room_id=room["id"],
        check_in_date=check_in,
        check_out_date=check_out,
    )

    assert result is not None


# ---------- FOREIGN KEY -----------


@pytest.mark.asyncio
async def test_booking_fk_guest(
    booking_repository,
    clean_database,
    room,
):
    with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
        await booking_repository.create(
            guest_id=999999,
            room_id=room["id"],
            check_in_date=date(2026, 10, 10),
            check_out_date=date(2026, 10, 15),
        )


@pytest.mark.asyncio
async def test_booking_fk_room(
    booking_repository,
    clean_database,
    guest,
):
    with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
        await booking_repository.create(
            guest_id=guest["id"],
            room_id=999999,
            check_in_date=date(2026, 10, 10),
            check_out_date=date(2026, 10, 15),
        )


@pytest.mark.asyncio
async def test_delete_guest_cascades_to_bookings(
    test_db,
    clean_database,
    guest,
    room,
):
    booking = await test_db.fetchrow(
        """
        INSERT INTO bookings (
            guest_id,
            room_id,
            check_in_date,
            check_out_date
        )
        VALUES ($1, $2, $3, $4)
        RETURNING id;
        """,
        guest["id"],
        room["id"],
        date(2026, 10, 10),
        date(2026, 10, 15),
    )

    await test_db.execute(
        "DELETE FROM guests WHERE id = $1",
        guest["id"],
    )

    result = await test_db.fetchrow(
        "SELECT * FROM bookings WHERE id = $1",
        booking["id"],
    )

    assert result is None


@pytest.mark.asyncio
async def test_delete_room_cascades_to_bookings(
    test_db,
    clean_database,
    guest,
    room,
):
    booking = await test_db.fetchrow(
        """
        INSERT INTO bookings (
            guest_id,
            room_id,
            check_in_date,
            check_out_date
        )
        VALUES ($1, $2, $3, $4)
        RETURNING id;
        """,
        guest["id"],
        room["id"],
        date(2026, 10, 10),
        date(2026, 10, 15),
    )

    await test_db.execute(
        "DELETE FROM rooms WHERE id = $1",
        room["id"],
    )

    result = await test_db.fetchrow(
        "SELECT * FROM bookings WHERE id = $1",
        booking["id"],
    )

    assert result is None
