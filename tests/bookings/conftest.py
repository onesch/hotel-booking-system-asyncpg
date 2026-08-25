from unittest.mock import AsyncMock
import pytest

from app.db_services.bookings import BookingRepository


@pytest.fixture
def booking_repository():
    repository = BookingRepository()
    repository.db.fetchrow = AsyncMock()
    repository.db.fetch = AsyncMock()
    return repository


@pytest.fixture
def booking_data():
    return {
        "id": 1,
        "guest_id": 1,
        "room_id": 1,
        "check_in_date": "2026-10-10",
        "check_out_date": "2026-10-15",
    }
