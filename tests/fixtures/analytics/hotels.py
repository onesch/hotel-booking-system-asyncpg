from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.db_services.analytics.hotels import HotelAnalyticsRepository
from app.db_services.hotels import HotelRepository
from app.services.analytics.hotels import HotelAnalyticsService


@pytest.fixture
def room_type_count_data():
    return {
        "room_type_id": 1,
        "room_type": "Standard",
        "room_count": 3,
    }


@pytest.fixture
def monthly_bookings_data():
    return {
        "month": datetime(2026, 8, 1),
        "booking_count": 4,
    }


@pytest.fixture
def room_type_popularity_data():
    return {
        "room_type_id": 1,
        "room_type": "Standard",
        "booking_count": 4,
    }


@pytest.fixture
def hotel_analytics_repository():
    repository = HotelAnalyticsRepository()
    repository.db = AsyncMock()
    return repository


@pytest.fixture
def hotel_analytics_service():
    service = HotelAnalyticsService()
    service.analytics_repo = AsyncMock(spec=HotelAnalyticsRepository)
    service.hotel_repo = AsyncMock(spec=HotelRepository)
    return service


@pytest.fixture
def api_hotel_analytics_service():
    return AsyncMock(spec=HotelAnalyticsService)
