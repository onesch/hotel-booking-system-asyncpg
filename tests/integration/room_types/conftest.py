import pytest

from app.settings import TEST_DATABASE_URL
from app.db_services.room_types import RoomTypeRepository


@pytest.fixture
def repository(monkeypatch):
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return RoomTypeRepository()
