from unittest.mock import AsyncMock

import pytest

from app.db_services.rooms import RoomRepository
from app.services.rooms import RoomService
from app.settings import settings


@pytest.fixture
def room_data():
    """
    Returns test data for a room.
    """
    return {
        "id": 1,
        "room_number": "101",
        "room_floor": "1",
        "is_active": True,
        "hotel_id": 1,
        "room_type_id": 1,
    }


@pytest.fixture
def api_room_service():
    """
    Returns a mocked RoomService for API tests.
    """
    return AsyncMock(spec=RoomService)


@pytest.fixture
def room_repository():
    """
    Returns a RoomRepository with a mocked database.
    """
    repository = RoomRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def integration_room_repository(monkeypatch):
    """
    Returns a RoomRepository configured to use the test database.
    """
    monkeypatch.setattr(
        settings,
        "database_url",
        settings.test_database_url,
    )
    return RoomRepository()


@pytest.fixture
def room_service():
    """
    Returns a RoomService with a mocked repository.
    """
    service = RoomService()
    service.repo = AsyncMock()
    return service
