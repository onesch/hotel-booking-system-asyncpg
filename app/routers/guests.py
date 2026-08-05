
from fastapi import APIRouter

from app.services.guests import GuestsServices
from app.schemas.guests import GuestCreate


router = APIRouter(tags=["guests"])

guests_service = GuestsServices()


@router.post("/create")
async def create_guest(
    guest: GuestCreate,
):
    """
    Create a new guest in the database.
    """
    return await guests_service.create(guest)
