from datetime import datetime

from app.db_services.guests import Guests
from app.schemas.guests import GuestCreate


class GuestsServices():
    """
    Service class for managing guests.
    """
    def __init__(self):
        self.repo = Guests()

    async def create(
        self,
        guest: GuestCreate,
    ) -> dict | None:
        """
        Create a new guest in the database.
        """

        return await self.repo.create(
            first_name=guest.first_name,
            last_name=guest.last_name,
            email=guest.email,
            phone=guest.phone,
        )
