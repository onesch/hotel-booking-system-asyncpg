import pytest
from unittest.mock import AsyncMock

from app.main import app
from app.services.guests import GuestService
from app.db_services.guests import GuestRepository
from app.settings import TEST_DATABASE_URL
from app.dependencies.auth import (
    get_current_guest,
    require_business,
)


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
def api_guest_service():
    """
    Returns a mocked GuestService for API tests.
    """
    return AsyncMock(spec=GuestService)


@pytest.fixture
def guest_repository():
    """
    Returns a GuestRepository with a mocked database.
    """
    repository = GuestRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def integration_guest_repository(monkeypatch):
    """
    Returns a GuestRepository configured to use the test database.
    """
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return GuestRepository()


@pytest.fixture
def guest_service():
    """
    Returns a GuestService with a mocked repository.
    """
    service = GuestService()
    service.repo = AsyncMock()
    return service


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
