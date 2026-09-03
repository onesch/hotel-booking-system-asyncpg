from app.db_services.bookings import BookingRepository
from app.exceptions.http import (
    ConflictException,
    NotFoundException,
)
from app.exceptions.database import RoomAlreadyBookedError
from app.schemas.bookings import (
    BookingCreate,
    BookingDelete,
    BookingUpdate,
)


class BookingService:
    """
    Service class for managing bookings.
    """

    def __init__(self):
        self.repo = BookingRepository()

    async def create(
        self,
        booking: BookingCreate,
        guest_id: int,
    ) -> dict | None:
        """
        Create a new booking.
        """
        try:
            return await self.repo.create(
                guest_id=guest_id,
                room_id=booking.room_id,
                check_in_date=booking.check_in_date,
                check_out_date=booking.check_out_date,
            )
        except RoomAlreadyBookedError as e:
            raise ConflictException(
                detail="Room is already booked for these dates"
            ) from e

    async def get_by_id(
        self,
        id: int,
    ) -> dict:
        """
        Get booking by id.
        """
        booking = await self.repo.get_by_id(id)

        if booking is None:
            raise NotFoundException(detail="Booking not found")

        return booking

    async def get_all(
        self,
    ) -> list[dict]:
        """
        Get all bookings.
        """
        return await self.repo.get_all()

    async def update(
        self,
        booking: BookingUpdate,
    ) -> dict:
        """
        Update booking.
        """
        try:
            updated_booking = await self.repo.update(
                id=booking.id,
                check_in_date=booking.check_in_date,
                check_out_date=booking.check_out_date,
            )
        except RoomAlreadyBookedError as e:
            raise ConflictException(
                detail="Room is already booked for these dates"
            ) from e

        if updated_booking is None:
            raise NotFoundException(detail="Booking not found")

        return updated_booking

    async def delete(
        self,
        booking: BookingDelete,
    ) -> dict:
        """
        Delete booking.
        """
        deleted_booking = await self.repo.delete(
            id=booking.id,
        )

        if deleted_booking is None:
            raise NotFoundException(detail="Booking not found")

        return deleted_booking
