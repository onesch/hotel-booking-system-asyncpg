from fastapi import HTTPException

from app.db_services.rooms import RoomRepository
from app.schemas.rooms import (
    RoomCreate,
    RoomDelete,
    RoomUpdate,
)


class RoomService:
    """
    Service class for managing rooms.
    """

    def __init__(self):
        self.repo = RoomRepository()

    async def create(
        self,
        room: RoomCreate,
    ) -> dict | None:
        """
        Create a new room.
        """
        return await self.repo.create(
            room_number=room.room_number,
            room_floor=room.room_floor,
            is_active=room.is_active,
            hotel_id=room.hotel_id,
            room_type_id=room.room_type_id,
        )

    async def get_by_id(
        self,
        room_id: int,
    ):
        """
        Get room by id.
        """
        room = await self.repo.get_by_id(room_id)

        if room is None:
            raise HTTPException(
                status_code=404,
                detail="Room not found",
            )

        return room

    async def get_all(self):
        """
        Get all rooms.
        """
        return await self.repo.get_all()

    async def update(
        self,
        room: RoomUpdate,
    ) -> dict:
        """
        Update room.
        """
        updated_room = await self.repo.update(
            id=room.id,
            room_number=room.room_number,
            room_floor=room.room_floor,
            is_active=room.is_active,
            hotel_id=room.hotel_id,
            room_type_id=room.room_type_id,
        )

        if updated_room is None:
            raise HTTPException(
                status_code=404,
                detail="Room not found",
            )

        return updated_room

    async def delete(
        self,
        room: RoomDelete,
    ):
        """
        Delete room.
        """
        deleted_room = await self.repo.delete(id=room.id)

        if deleted_room is None:
            raise HTTPException(
                status_code=404,
                detail="Room not found",
            )

        return deleted_room
