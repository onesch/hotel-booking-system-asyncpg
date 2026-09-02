import pytest
from unittest.mock import AsyncMock

from app.main import app
from app.dependencies.auth import require_business
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
        "owner_id": 1,
    }


@pytest.fixture
def business_guest(hotel_data):
    return {
        "id": hotel_data["owner_id"],
        "role": "business",
    }


@pytest.fixture
def override_business_guest(business_guest):
    app.dependency_overrides[require_business] = (
        lambda: business_guest
    )

    yield business_guest

    app.dependency_overrides.clear()


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
