from app.db_services.analytics.hotels import HotelAnalyticsRepository
from app.db_services.hotels import HotelRepository
from app.exceptions.http import NotFoundException


class HotelAnalyticsService:
    """
    Provides business logic for hotel analytics.
    """

    def __init__(self):
        self.analytics_repo = HotelAnalyticsRepository()
        self.hotel_repo = HotelRepository()

    async def room_type_counts(
        self,
        hotel_id: int,
    ) -> list[dict]:
        """
        Return the number of rooms grouped by room type for a hotel.

        Returns:
            List of room types with their room counts.
        """
        hotel = await self.hotel_repo.get_by_id(hotel_id)

        if hotel is None:
            raise NotFoundException(
                detail="Hotel not found"
            )

        return await self.analytics_repo.room_type_counts(hotel_id)

    async def monthly_bookings(
        self,
        hotel_id: int,
    ) -> list[dict]:
        """
        Return booking counts grouped by month for a hotel.

        Returns:
            List of months with their booking counts.
        """
        hotel = await self.hotel_repo.get_by_id(hotel_id)

        if hotel is None:
            raise NotFoundException(
                detail="Hotel not found"
            )

        return await self.analytics_repo.monthly_bookings(hotel_id)

    async def room_type_popularity(
        self,
        hotel_id: int,
    ) -> list[dict]:
        """
        Return room types ordered by booking count for a hotel.

        Returns:
            List of room types with their booking counts.
        """
        hotel = await self.hotel_repo.get_by_id(hotel_id)

        if hotel is None:
            raise NotFoundException(
                detail="Hotel not found"
            )

        return await self.analytics_repo.room_type_popularity(hotel_id)
