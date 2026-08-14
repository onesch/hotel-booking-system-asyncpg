from fastapi import HTTPException

from app.db_services.guests import GuestRepository
from app.schemas.guests import (
    GuestDelete,
    GuestUpdate,
)


class GuestService():
    """
    Service class for managing guests.
    """

    def __init__(self):
        self.repo = GuestRepository()

    async def get_by_id(
        self,
        guest_id: int,
    ):
        """
        Get guest by id.
        """
        guest = await self.repo.get_by_id(guest_id)

        if guest is None:
            raise HTTPException(
                status_code=404,
                detail="Guest not found",
            )
        return guest

    async def get_by_email(self, email: str):
        """
        Get guest by email.
        """
        return await self.repo.get_by_email(email)

    async def get_all(self):
        """
        Get all guests.
        """
        return await self.repo.get_all()

    async def update(
        self,
        guest: GuestUpdate,
    ) -> dict:
        """
        Update guest.
        """
        updated_guest = await self.repo.update(
            id=guest.id,
            first_name=guest.first_name,
            last_name=guest.last_name,
            email=guest.email,
            phone=guest.phone,
            role=guest.role,
            password_hash=guest.password_hash,
        )

        if updated_guest is None:
            raise HTTPException(
                status_code=404,
                detail="Guest not found",
            )

        return updated_guest

    async def delete(
        self,
        guest: GuestDelete,
    ):
        """
        Delete guest.
        """
        deleted_guest = await self.repo.delete(id=guest.id)

        if deleted_guest is None:
            raise HTTPException(
                status_code=404,
                detail="Guest not found",
            )

        return deleted_guest
