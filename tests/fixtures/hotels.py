import pytest
from unittest.mock import AsyncMock

from app.services.hotels import HotelService
from app.db_services.hotels import HotelRepository
from app.settings import TEST_DATABASE_URL


@pytest.fixture
def hotel_data():
    """
    Returns test data for a hotel.
    """
    return {
        "id": 1,
        "name": "HotelName",
        "address": "Hotel st. 123",
        "description": "HotelDescription",
        "owner_id": 1,
    }


@pytest.fixture
def api_hotel_service():
    """
    Returns a mocked HotelService for API tests.
    """
    return AsyncMock(spec=HotelService)


@pytest.fixture
def hotel_repository():
    """
    Returns a HotelRepository with a mocked database.
    """
    repository = HotelRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def integration_hotel_repository(monkeypatch):
    """
    Returns a HotelRepository configured to use the test database.
    """
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return HotelRepository()


@pytest.fixture
def hotel_service():
    """
    Returns a HotelService with a mocked repository.
    """
    service = HotelService()
    service.repo = AsyncMock()
    return service
