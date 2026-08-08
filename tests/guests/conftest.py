import pytest
from unittest.mock import AsyncMock

from app.db_services.guests import GuestRepository
from app.services.guests import GuestService


@pytest.fixture
def guest_data():
    """
    Returns test data for a guest.
    """
    return {
        "id": 1,
        "first_name": "Name",
        "last_name": "LastName",
        "email": "example@email.com",
        "phone": "123456789",
    }


@pytest.fixture
def guest_repository():
    """
    Returns a GuestRepository with a mocked database.
    """
    repository = GuestRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def guest_service():
    """
    Returns a GuestService with a mocked repository.
    """
    service = GuestService()
    service.repo = AsyncMock()
    return service


@pytest.fixture
def api_guest_service():
    """
    Returns a mocked GuestService for API tests.
    """
    return AsyncMock(spec=GuestService)
