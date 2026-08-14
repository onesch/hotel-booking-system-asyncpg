from fastapi import APIRouter

from app.services.auth import AuthService
from app.schemas.guests import (
    GuestRegister,
    GuestResponse,
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
