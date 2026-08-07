from fastapi import HTTPException

from app.db_services.hotels import Hotels
from app.schemas.hotels import (
    HotelCreate,
    HotelDelete,
    HotelUpdate,
)


class HotelsServices:
    """
    Service class for managing hotels.
    """

    def __init__(self):
        self.repo = Hotels()

    async def create(
        self,
        hotel: HotelCreate,
    ) -> dict | None:
        """
        Create a new hotel.
        """
        return await self.repo.create(
            name=hotel.name,
            address=hotel.address,
            description=hotel.description,
        )

    async def get_by_id(
        self,
        hotel_id: int,
    ) -> dict:
        """
        Get hotel by id.
        """
        hotel = await self.repo.get_by_id(hotel_id)

        if hotel is None:
            raise HTTPException(
                status_code=404,
                detail="Hotel not found",
            )

        return hotel

    async def get_all(
        self,
    ) -> list[dict]:
        """
        Get all hotels.
        """
        return await self.repo.get_all()

    async def update(
        self,
        hotel: HotelUpdate,
    ) -> dict:
        """
        Update hotel.
        """
        updated_hotel = await self.repo.update(
            id=hotel.id,
            name=hotel.name,
            address=hotel.address,
            description=hotel.description,
        )

        if updated_hotel is None:
            raise HTTPException(
                status_code=404,
                detail="Hotel not found",
            )

        return updated_hotel

    async def delete(
        self,
        hotel: HotelDelete,
    ):
        """
        Delete hotel.
        """
        deleted_hotel = await self.repo.delete(id=hotel.id)

        if deleted_hotel is None:
            raise HTTPException(
                status_code=404,
                detail="Hotel not found",
            )

        return deleted_hotel
