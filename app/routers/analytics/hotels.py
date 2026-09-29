from fastapi import APIRouter

from app.services.analytics.hotels import HotelAnalyticsService
from app.schemas.analytics.hotels import (
    MonthlyBookingsResponse,
    RoomTypeCountResponse,
    RoomTypePopularityResponse,
)


router = APIRouter(tags=["hotel-analytics"])

hotel_analytics_service = HotelAnalyticsService()


@router.get(
    "/{hotel_id}/room-types/count",
    response_model=list[RoomTypeCountResponse]
)
async def get_room_type_counts(hotel_id: int):
    """
    Get room type count by hotel id.
    """
    return await hotel_analytics_service.room_type_counts(hotel_id)


@router.get(
    "/{hotel_id}/bookings/monthly",
    response_model=list[MonthlyBookingsResponse],
)
async def get_monthly_bookings(hotel_id: int):
    """
    Get monthly booking counts by hotel id.
    """
    return await hotel_analytics_service.monthly_bookings(hotel_id)


@router.get(
    "/{hotel_id}/room-types/popularity",
    response_model=list[RoomTypePopularityResponse],
)
async def get_room_type_popularity(hotel_id: int):
    """
    Get room type popularity by hotel id.
    """
    return await hotel_analytics_service.room_type_popularity(hotel_id)
