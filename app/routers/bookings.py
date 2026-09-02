from fastapi import APIRouter, Depends

from app.dependencies.auth import (
    get_current_guest,
    require_owner_or_admin,
)
from app.services.bookings import BookingService
from app.schemas.bookings import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
    BookingDelete,
)


router = APIRouter(tags=["bookings"])

bookings_service = BookingService()


@router.post("/create", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    current_guest=Depends(get_current_guest),
):
    """
    Create a new booking.
    """
    return await bookings_service.create(
        booking=booking,
        guest_id=current_guest["id"],
    )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
    booking_id: int,
):
    """
    Get booking by id.
    """
    return await bookings_service.get_by_id(booking_id)


@router.get("/", response_model=list[BookingResponse])
async def get_bookings():
    """
    Get all bookings.
    """
    return await bookings_service.get_all()


@router.patch("/update", response_model=BookingResponse)
async def update_booking(
    booking: BookingUpdate,
    current_guest=Depends(get_current_guest),
):
    """
    Update booking.
    """
    existing_booking = await bookings_service.get_by_id(booking.id)
    require_owner_or_admin(
        current_guest, owner_id=existing_booking["guest_id"],
    )

    return await bookings_service.update(
        booking=booking,
        guest_id=current_guest["id"],
    )


@router.delete("/delete", response_model=BookingResponse)
async def delete_booking(
    booking: BookingDelete,
    current_guest=Depends(get_current_guest),
):
    """
    Delete booking.
    """
    existing_booking = await bookings_service.get_by_id(booking.id)
    require_owner_or_admin(
        current_guest, owner_id=existing_booking["guest_id"],
    )

    return await bookings_service.delete(
        booking_id=booking.id,
        guest_id=current_guest["id"],
    )
