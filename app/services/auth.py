from app.db_services.guests import GuestRepository
from app.schemas.guests import GuestRegister
from app.security import hash_password, verify_password


class AuthService:
    """
    Service class manages guest authentication and authorization.
    """

    def __init__(self):
        self.guest_repo = GuestRepository()

    async def register(
        self,
        guest: GuestRegister,
    ):
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
