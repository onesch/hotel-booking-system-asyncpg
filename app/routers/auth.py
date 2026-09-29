from fastapi import APIRouter, HTTPException

from app.schemas.guests import GuestResponse
from app.services.auth import AuthService
from app.schemas.auth import (
    BusinessRegister,
    BusinessRegisterResponse,
    GuestRegister,
    GuestRegisterResponse,
    LoginRequest,
)


router = APIRouter(tags=["auth"])

auth_service = AuthService()


@router.post("/register", response_model=GuestRegisterResponse)
async def register(
    guest: GuestRegister,
):
    """
    Register a new guest.
    """
    response = await auth_service.register(guest)

    response["message"] = "Successful registration."

    return response


@router.post("/register/business", response_model=BusinessRegisterResponse)
async def register_business(
    business: BusinessRegister,
):
    """
    Register a business account.
    """
    response = await auth_service.register_business(business)

    response["message"] = "Successful registration."

    return response


@router.post("/login", response_model=GuestResponse)
async def login(
    credentials: LoginRequest,
):
    """
    Authenticate a guest.
    """
    guest = await auth_service.authenticate(
        email=credentials.email,
        password=credentials.password.get_secret_value(),
    )

    if not guest:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return guest
