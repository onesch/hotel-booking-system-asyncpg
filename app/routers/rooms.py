from fastapi import APIRouter, Depends

from app.dependencies.auth import require_business
from app.services.rooms import RoomService
from app.schemas.rooms import (
    RoomCreate,
    RoomResponse,
    RoomUpdate,
    RoomDelete,
)


router = APIRouter(tags=["rooms"])

rooms_service = RoomService()


@router.post("/create")
async def create_room(
    room: RoomCreate,
    current_guest=Depends(require_business),
):
    """
    Create a new room.
    Only business account can access this endpoint.
    """
    return await rooms_service.create(room)


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room_by_id(
    room_id: int,
):
    """
    Get room by id.
    """
    return await rooms_service.get_by_id(room_id)


@router.get("/", response_model=list[RoomResponse])
async def get_rooms():
    """
    Get all rooms.
    """
    return await rooms_service.get_all()


@router.patch("/update")
async def update_room(
    room: RoomUpdate,
    current_guest=Depends(require_business),
):
    """
    Update room.
    Only business account can access this endpoint.
    """
    return await rooms_service.update(room)


@router.delete("/delete")
async def delete_room(
    room: RoomDelete,
    current_guest=Depends(require_business),
):
    """
    Delete room.
    Only business account can access this endpoint.
    """
    return await rooms_service.delete(room)
