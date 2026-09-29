import asyncpg
from app.exceptions.database import RoomAlreadyBookedError

from app.db import Database


class BookingRepository():
    def __init__(self):
        self.db = Database()

    async def create(
            self,
            guest_id: int,
            room_id: int,
            check_in_date: str,
            check_out_date: str,
    ) -> dict | None:
        query = """
            INSERT INTO bookings (
                guest_id,
                room_id,
                check_in_date,
                check_out_date
            )
            VALUES ($1, $2, $3, $4)
            RETURNING *;
        """
        try:
            booking = await self.db.fetchrow(
                query,
                guest_id,
                room_id,
                check_in_date,
                check_out_date,
            )
            return booking
        except asyncpg.exceptions.ExclusionViolationError as e:
            raise RoomAlreadyBookedError from e

    async def get_by_id(self, id: int) -> dict | None:
        query = """
            SELECT
                id,
                guest_id,
                room_id,
                check_in_date,
                check_out_date
            FROM bookings
            WHERE id = $1;
        """
        return await self.db.fetchrow(query, id)

    async def get_all(self) -> list[dict]:
        query = """
            SELECT
                id,
                guest_id,
                room_id,
                check_in_date,
                check_out_date
            FROM bookings
            ORDER BY id;
        """
        return await self.db.fetch(query)

    async def update(
        self,
        id: int,
        check_in_date: str,
        check_out_date: str,
    ) -> dict | None:
        query = """
            UPDATE bookings
            SET
                check_in_date = $2,
                check_out_date = $3
            WHERE id = $1
            RETURNING *;
        """
        try:
            return await self.db.fetchrow(
                query,
                id,
                check_in_date,
                check_out_date,
            )
        except asyncpg.exceptions.ExclusionViolationError as e:
            raise RoomAlreadyBookedError from e

    async def delete(self, id: int) -> dict | None:
        query = """
            DELETE FROM bookings
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(query, id)
