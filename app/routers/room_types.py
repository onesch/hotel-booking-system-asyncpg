from fastapi import APIRouter, Depends

from app.dependencies.auth import require_admin
from app.services.room_types import RoomTypeService
from app.schemas.room_types import (
    RoomTypeCreate,
    RoomTypeResponse,
    RoomTypeUpdate,
    RoomTypeDelete,
)


router = APIRouter(tags=["room-types"])

room_types_service = RoomTypeService()


@router.post("/create")
async def create_room_type(
    room_type: RoomTypeCreate,
    current_guest=Depends(require_admin),
):
    """
    Create a new room type.
    Only admin's can access this endpoint.
    """
    return await room_types_service.create(room_type)


@router.get("/{room_type_id}", response_model=RoomTypeResponse)
async def get_room_type_by_id(
    room_type_id: int,
):
    """
    Get room type by id.
    """
    return await room_types_service.get_by_id(room_type_id)


@router.get("/", response_model=list[RoomTypeResponse])
async def get_room_types():
    """
    Get all room types.
    """
    return await room_types_service.get_all()


@router.patch("/update")
async def update_room_type(
    room_type: RoomTypeUpdate,
    current_guest=Depends(require_admin),
):
    """
    Update room type.
    Only admin's can access this endpoint.
    """
    return await room_types_service.update(room_type)


@router.delete("/delete")
async def delete_room_type(
    room_type: RoomTypeDelete,
    current_guest=Depends(require_admin),
):
    """
    Delete room type.
    Only admin's can access this endpoint.
    """
    return await room_types_service.delete(room_type)
