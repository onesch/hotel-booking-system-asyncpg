
from fastapi import APIRouter

from app.services.hotels import HotelService
from app.schemas.hotels import (
    HotelCreate,
    HotelResponse,
    HotelUpdate,
    HotelDelete,
)


router = APIRouter(tags=["hotels"])

hotels_service = HotelService()


@router.post("/create")
async def create_hotel(
    hotel: HotelCreate,
):
    """
    Create a new hotel.
    """
    return await hotels_service.create(hotel)


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel_by_id(
    hotel_id: int,
):
    """
    Get hotel by id.
    """
    return await hotels_service.get_by_id(hotel_id)


@router.get("/", response_model=list[HotelResponse])
async def get_hotels():
    """
    Get all hotels.
    """
    return await hotels_service.get_all()


@router.patch("/update")
async def update_hotel(
    hotel: HotelUpdate,
):
    """
    Update hotel.
    """
    return await hotels_service.update(hotel)


@router.delete("/delete")
async def delete_hotel(
    hotel: HotelDelete,
):
    """
    Delete hotel.
    """
    return await hotels_service.delete(hotel)
