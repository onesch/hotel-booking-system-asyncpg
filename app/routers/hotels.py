
from fastapi import APIRouter, Depends

from app.services.hotels import HotelService
from app.dependencies.auth import (
    require_business,
    require_owner_or_admin,
)
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
    current_guest=Depends(require_business),
):
    """
    Create a new hotel.
    Only business account can access this endpoint.
    """
    return await hotels_service.create(
        hotel=hotel,
        owner_id=current_guest["id"],
    )


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
    current_guest=Depends(require_business),
):
    """
    Update hotel.
    Only business account can access this endpoint.
    """
    existing_hotel = await hotels_service.get_by_id(hotel.id)
    require_owner_or_admin(
        current_guest, owner_id=existing_hotel["owner_id"],
    )

    return await hotels_service.update(hotel)


@router.delete("/delete")
async def delete_hotel(
    hotel: HotelDelete,
    current_guest=Depends(require_business),
):
    """
    Delete hotel.
    Only business account can access this endpoint.
    """
    existing_hotel = await hotels_service.get_by_id(hotel.id)
    require_owner_or_admin(
        current_guest, owner_id=existing_hotel["owner_id"],
    )

    return await hotels_service.delete(hotel)
