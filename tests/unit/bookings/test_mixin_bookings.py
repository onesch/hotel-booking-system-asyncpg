import pytest
from datetime import date

from app.schemas.bookings import BookingCreate


@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (date(2026, 10, 10), date(2026, 10, 15)),
        (date(2026, 10, 10), date(2026, 10, 11)),
        (date(2026, 10, 15), date(2026, 10, 20)),
    ],
)
def test_booking_dates_valid(check_in, check_out):
    booking = BookingCreate(
        guest_id=1,
        room_id=1,
        check_in_date=check_in,
        check_out_date=check_out,
    )

    assert booking.check_in_date == check_in
    assert booking.check_out_date == check_out


@pytest.mark.parametrize(
    "check_in, check_out",
    [
        # Same day
        (date(2026, 10, 10), date(2026, 10, 10)),
        # Reversed
        (date(2026, 10, 15), date(2026, 10, 10)),
        # One day backwards
        (date(2026, 10, 15), date(2026, 10, 14)),
    ],
)
def test_booking_dates_invalid(check_in, check_out):
    with pytest.raises(
        ValueError,
        match="Check-out date must be after check-in date"
    ):
        BookingCreate(
            guest_id=1,
            room_id=1,
            check_in_date=check_in,
            check_out_date=check_out,
        )
