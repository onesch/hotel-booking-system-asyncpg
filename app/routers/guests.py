from fastapi import APIRouter

from app.services.guests import GuestService
from app.schemas.guests import (
    GuestCreate,
    GuestResponse,
    GuestUpdate,
    GuestDelete,
)


router = APIRouter(tags=["guests"])

guests_service = GuestService()


@router.post("/create")
async def create_guest(
    guest: GuestCreate,
):
    """
    Create a new guest.
    """
    return await guests_service.create(guest)


@router.get("/{guest_id}", response_model=GuestResponse)
async def get_guest_by_id(
    guest_id: int,
):
    """
    Get guest by id.
    """
    return await guests_service.get_by_id(guest_id)


@router.get("/", response_model=list[GuestResponse])
async def get_guests():
    """
    Get all guests.
    """
    return await guests_service.get_all()


@router.patch("/update")
async def update_guest(
    guest: GuestUpdate,
):
    """
    Update guest.
    """
    return await guests_service.update(guest)


@router.delete("/delete")
async def delete_guest(
    guest: GuestDelete,
):
    """
    Delete guest.
    """
    return await guests_service.delete(guest)
