import pytest
from unittest.mock import AsyncMock

from app.db_services.hotels import HotelRepository
from app.services.hotels import HotelService


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
    }


@pytest.fixture
def hotel_repository():
    """
    Returns a HotelRepository with a mocked database.
    """
    repository = HotelRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def hotel_service():
    """
    Returns a HotelService with a mocked repository.
    """
    service = HotelService()
    service.repo = AsyncMock()
    return service


@pytest.fixture
def api_hotel_service():
    """
    Returns a mocked HotelService for API tests.
    """
    return AsyncMock(spec=HotelService)
