import pytest
import datetime
from unittest.mock import AsyncMock

from app.services.bookings import BookingService
from app.db_services.bookings import BookingRepository
from app.settings import TEST_DATABASE_URL


@pytest.fixture
def booking_data():
    """
    Returns booking test data.
    """
    return {
        "id": 1,
        "guest_id": 1,
        "room_id": 1,
        "check_in_date": datetime.date(2026, 10, 10),
        "check_out_date": datetime.date(2026, 10, 15),
    }


@pytest.fixture
def api_booking_service():
    """
    Returns a mocked BookingService for API tests.
    """
    return AsyncMock(spec=BookingService)


@pytest.fixture
def booking_repository():
    """
    Returns a BookingRepository with a mocked database.
    """
    repository = BookingRepository()
    repository.db.fetchrow = AsyncMock()
    repository.db.fetch = AsyncMock()
    return repository



@pytest.fixture
def integration_booking_repository(monkeypatch):
    """
    Returns a BookingRepository configured to use the test database.
    """
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return BookingRepository()


@pytest.fixture
def booking_service():
    """
    Returns a BookingService with a mocked repository.
    """
    service = BookingService()
    service.repo = AsyncMock()
    return service
