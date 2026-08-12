import asyncpg
from fastapi import HTTPException

from app.db import Database


class RoomTypeRepository:
    """
    Class for managing room types in the database.
    """

    def __init__(self):
        self.db = Database()

    async def create(
        self,
        room_type: str,
    ) -> dict | None:
        query = """
            INSERT INTO room_types (
                room_type
            )
            VALUES ($1)
            RETURNING *;
        """
        try:
            return await self.db.fetchrow(
                query,
                room_type,
            )

        except asyncpg.exceptions.CheckViolationError:
            raise HTTPException(
                status_code=400,
                detail="Invalid room type",
            )

    async def get_by_id(
        self,
        room_type_id: int,
    ) -> dict | None:
        query = """
            SELECT
                id,
                room_type
            FROM room_types
            WHERE id = $1;
        """
        return await self.db.fetchrow(query, room_type_id)

    async def get_all(
        self,
    ) -> list[dict]:
        query = """
            SELECT
                id,
                room_type
            FROM room_types;
        """
        return await self.db.fetch(query)

    async def update(
        self,
        id: int,
        room_type: str | None,
    ) -> dict | None:
        query = """
            UPDATE room_types
            SET
                room_type = COALESCE($2, room_type)
            WHERE id = $1
            RETURNING *;
        """
        try:
            return await self.db.fetchrow(
                query,
                id,
                room_type,
            )

        except asyncpg.exceptions.CheckViolationError:
            raise HTTPException(
                status_code=400,
                detail="Invalid room type",
            )

    async def delete(
        self,
        id: int,
    ) -> dict | None:
        query = """
            DELETE FROM room_types
            WHERE id = $1
            RETURNING *;
        """
        try:
            return await self.db.fetchrow(query, id)

        except asyncpg.exceptions.ForeignKeyViolationError:
            raise HTTPException(
                status_code=409,
                detail="Room type is used by one or more rooms",
            )
