import asyncpg
from app.exceptions.database import RelatedEntityNotFoundError

from app.db import Database


class RoomRepository:
    """
    Class for managing rooms in the database.
    """

    def __init__(self):
        self.db = Database()

    async def create(
        self,
        room_number: str,
        room_floor: str,
        is_active: bool,
        hotel_id: int,
        room_type_id: int,
    ) -> dict | None:
        query = """
            INSERT INTO rooms (
                room_number,
                room_floor,
                is_active,
                hotel_id,
                room_type_id
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *;
        """
        try:
            room = await self.db.fetchrow(
                query,
                room_number,
                room_floor,
                is_active,
                hotel_id,
                room_type_id,
            )
            return room
        except asyncpg.exceptions.ForeignKeyViolationError as e:
            raise RelatedEntityNotFoundError from e

    async def get_by_id(self, id: int) -> dict | None:
        query = """
            SELECT
                id,
                room_number,
                room_floor,
                is_active,
                hotel_id,
                room_type_id
            FROM rooms
            WHERE id = $1;
        """
        return await self.db.fetchrow(query, id)

    async def get_all(self) -> list[dict]:
        query = """
            SELECT
                id,
                room_number,
                room_floor,
                is_active,
                hotel_id,
                room_type_id
            FROM rooms;
        """
        return await self.db.fetch(query)

    async def update(
        self,
        id: int,
        room_number: str | None,
        room_floor: str | None,
        is_active: bool | None,
        hotel_id: int | None,
        room_type_id: int | None,
    ) -> dict | None:
        query = """
            UPDATE rooms
            SET
                room_number = COALESCE($2, room_number),
                room_floor = COALESCE($3, room_floor),
                is_active = COALESCE($4, is_active),
                hotel_id = COALESCE($5, hotel_id),
                room_type_id = COALESCE($6, room_type_id)
            WHERE id = $1
            RETURNING *;
        """
        try:
            room = await self.db.fetchrow(
                query,
                id,
                room_number,
                room_floor,
                is_active,
                hotel_id,
                room_type_id,
            )

            return room

        except asyncpg.exceptions.ForeignKeyViolationError as e:
            raise RelatedEntityNotFoundError from e

    async def delete(self, id: int) -> dict | None:
        query = """
            DELETE FROM rooms
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(query, id)
