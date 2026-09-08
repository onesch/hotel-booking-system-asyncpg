import pytest

from app.main import app
from app.dependencies.auth import get_current_guest


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
