from fastapi import HTTPException

from app.db_services.room_types import RoomTypeRepository
from app.schemas.room_types import (
    RoomTypeCreate,
    RoomTypeDelete,
    RoomTypeUpdate,
)


class RoomTypeService:
    """
    Service class for managing room types.
    """

    def __init__(self):
        self.repo = RoomTypeRepository()

    async def create(
        self,
        room_type: RoomTypeCreate,
    ) -> dict | None:
        """
        Create a new room type.
        """
        return await self.repo.create(room_type=room_type.room_type)

    async def get_by_id(
        self,
        room_type_id: int,
    ):
        """
        Get room type by id.
        """
        room_type = await self.repo.get_by_id(room_type_id)

        if room_type is None:
            raise HTTPException(
                status_code=404,
                detail="Room type not found",
            )

        return room_type

    async def get_all(self):
        """
        Get all room types.
        """
        return await self.repo.get_all()

    async def update(
        self,
        room_type: RoomTypeUpdate,
    ) -> dict:
        """
        Update room type.
        """
        updated_room_type = await self.repo.update(
            id=room_type.id,
            room_type=room_type.room_type,
        )

        if updated_room_type is None:
            raise HTTPException(
                status_code=404,
                detail="Room type not found",
            )

        return updated_room_type

    async def delete(
        self,
        room_type: RoomTypeDelete,
    ):
        """
        Delete room type.
        """
        deleted_room_type = await self.repo.delete(id=room_type.id)

        if deleted_room_type is None:
            raise HTTPException(
                status_code=404,
                detail="Room type not found",
            )

        return deleted_room_type
