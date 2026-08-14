import pytest
from unittest.mock import AsyncMock

from app.main import app
from app.dependencies.auth import get_current_guest
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
def current_guest(guest_data):
    return {
        "id": guest_data["id"],
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
def admin_guest():
    return {
        "id": 1,
        "role": "admin",
    }


@pytest.fixture
def override_admin_guest(admin_guest):
    app.dependency_overrides[get_current_guest] = (
        lambda: admin_guest
    )

    yield admin_guest

    app.dependency_overrides.clear()


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
