from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_guest, require_owner_or_admin
from app.services.guests import GuestService
from app.schemas.guests import (
    GuestResponse,
    GuestUpdate,
    GuestDelete,
)


router = APIRouter(tags=["guests"])

guests_service = GuestService()


@router.get("/{guest_id}", response_model=GuestResponse)
async def get_guest_by_id(
    guest_id: int,
):
    """
    Get guest by id.
    """
    return await guests_service.get_by_id(guest_id)


@router.get("/email/{guest_email}", response_model=GuestResponse)
async def get_guest_by_email(
    guest_email: str,
):
    """
    Get guest by email.
    """
    return await guests_service.get_by_email(guest_email)


@router.get("/", response_model=list[GuestResponse])
async def get_guests():
    """
    Get all guests.
    """
    return await guests_service.get_all()


@router.patch("/update")
async def update_guest(
    guest: GuestUpdate,
    current_guest=Depends(get_current_guest),
):
    """
    Update guest.
    """
    require_owner_or_admin(
        current_guest, owner_id=guest.id,
    )

    return await guests_service.update(guest)


@router.delete("/delete")
async def delete_guest(
    guest: GuestDelete,
    current_guest=Depends(get_current_guest),
):
    """
    Delete guest.
    """
    require_owner_or_admin(
        current_guest, owner_id=guest.id,
    )

    return await guests_service.delete(guest)
