import pytest

from app.settings import TEST_DATABASE_URL
from app.db_services.guests import GuestRepository


@pytest.fixture
def repository(monkeypatch):
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return GuestRepository()
