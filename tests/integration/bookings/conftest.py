import pytest

from app.settings import TEST_DATABASE_URL
from app.db_services.bookings import BookingRepository


@pytest.fixture
def booking_repository(monkeypatch):
    monkeypatch.setattr(
        "app.db.DATABASE_URL",
        TEST_DATABASE_URL,
    )

    return BookingRepository()
