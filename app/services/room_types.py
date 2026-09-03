from app.db_services.room_types import RoomTypeRepository
from app.exceptions.http import (
    NotFoundException,
    ConflictException,
)
from app.exceptions.database import RoomTypeInUseError
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
            raise NotFoundException(detail="Room type not found")

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
            raise NotFoundException(detail="Room type not found")

        return updated_room_type

    async def delete(
        self,
        room_type: RoomTypeDelete,
    ):
        """
        Delete room type.
        """
        try:
            deleted_room_type = await self.repo.delete(id=room_type.id)
        except RoomTypeInUseError as e:
            raise ConflictException(
                detail="Room type is used by one or more rooms"
            ) from e

        if deleted_room_type is None:
            raise NotFoundException(detail="Room type not found")

        return deleted_room_type
