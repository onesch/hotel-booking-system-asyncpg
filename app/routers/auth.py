from fastapi import APIRouter

from app.services.auth import AuthService
from app.schemas.guests import GuestResponse
from app.schemas.auth import (
    BusinessRegisterResponse,
    GuestRegister,
    BusinessRegister,
)


router = APIRouter(tags=["auth"])

auth_service = AuthService()


@router.post("/register", response_model=GuestResponse)
async def register(
    guest: GuestRegister,
):
    """
    Register a new guest.
    """
    return await auth_service.register(guest)


@router.post("/register/business", response_model=BusinessRegisterResponse)
async def register_business(
    business: BusinessRegister,
):
    """
    Register a business account with a hotel.
    """
    return await auth_service.register_business(business)
