from fastapi import APIRouter

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
):
    """
    Create a new room.
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
):
    """
    Update room.
    """
    return await rooms_service.update(room)


@router.delete("/delete")
async def delete_room(
    room: RoomDelete,
):
    """
    Delete room.
    """
    return await rooms_service.delete(room)
