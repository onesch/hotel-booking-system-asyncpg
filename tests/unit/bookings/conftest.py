import datetime
from unittest.mock import AsyncMock
import pytest

from app.main import app
from app.dependencies.auth import get_current_guest
from app.db_services.bookings import BookingRepository
from app.services.bookings import BookingService


@pytest.fixture
def current_guest(booking_data):
    return {
        "id": booking_data["guest_id"],
        "role": "user",
    }


@pytest.fixture
def override_current_guest(current_guest):
    app.dependency_overrides[get_current_guest] = (
        lambda: current_guest
    )

    yield current_guest

    app.dependency_overrides.clear()


@pytest.fixture
def booking_repository():
    repository = BookingRepository()
    repository.db.fetchrow = AsyncMock()
    repository.db.fetch = AsyncMock()
    return repository


@pytest.fixture
def booking_service():
    """
    Returns a BookingService with a mocked repository.
    """
    service = BookingService()
    service.repo = AsyncMock()
    return service


@pytest.fixture
def api_booking_service():
    """
    Returns a mocked BookingService for API tests.
    """
    return AsyncMock(spec=BookingService)


@pytest.fixture
def booking_data():
    return {
        "id": 1,
        "guest_id": 1,
        "room_id": 1,
        "check_in_date": datetime.date(2026, 10, 10),
        "check_out_date": datetime.date(2026, 10, 15),
    }
