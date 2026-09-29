import pytest
from unittest.mock import AsyncMock

from app.services.room_types import RoomTypeService
from app.db_services.room_types import RoomTypeRepository
from app.settings import settings


@pytest.fixture
def room_type_data():
    """
    Returns test data for a room type.
    """
    return {
        "id": 1,
        "room_type": "Standard",
    }


@pytest.fixture
def api_room_type_service():
    """
    Returns a mocked RoomTypeService for API tests.
    """
    return AsyncMock(spec=RoomTypeService)


@pytest.fixture
def room_type_repository():
    """
    Returns a RoomTypeRepository with a mocked database.
    """
    repository = RoomTypeRepository()
    repository.db = AsyncMock()

    return repository


@pytest.fixture
def integration_room_type_repository(monkeypatch):
    """
    Returns a RoomTypeRepository configured to use the test database.
    """
    monkeypatch.setattr(
        settings,
        "database_url",
        settings.test_database_url,
    )

    return RoomTypeRepository()


@pytest.fixture
def room_type_service():
    """
    Returns a RoomTypeService with a mocked repository.
    """
    service = RoomTypeService()
    service.repo = AsyncMock()

    return service
