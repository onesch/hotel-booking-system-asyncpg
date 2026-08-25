from app.db_services.guests import GuestRepository
from app.db_services.hotels import HotelRepository
from app.security import hash_password, verify_password
from app.schemas.auth import (
    GuestRegister,
    BusinessRegister,
)


class AuthService:
    """
    Service class manages authentication and authorization
    """

    def __init__(self):
        self.guest_repo = GuestRepository()
        self.hotel_repo = HotelRepository()

    async def register(
        self,
        guest: GuestRegister,
    ) -> dict | None:
        """
        Register a guest with a hashed password.
        """
        password_hash = hash_password(guest.password)

        return await self.guest_repo.create(
            first_name=guest.first_name,
            last_name=guest.last_name,
            email=guest.email,
            phone=guest.phone,
            password_hash=password_hash,
        )

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> dict | None:
        """
        Authenticate a guest by email and password.
        """
        guest = await self.guest_repo.get_by_email(email)

        if not guest:
            return None

        if not verify_password(
            password,
            guest["password_hash"],
        ):
            return None

        return guest

    async def register_business(
        self,
        business: BusinessRegister,
    ) -> dict[str, dict | None]:
        """
        Register a business account.
        """
        password_hash = hash_password(business.password)

        guest = await self.guest_repo.create_business(
            first_name=business.first_name,
            last_name=business.last_name,
            email=business.email,
            phone=business.phone,
            password_hash=password_hash,
        )

        return guest
