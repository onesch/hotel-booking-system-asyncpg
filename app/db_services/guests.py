import asyncpg
from fastapi import HTTPException

from app.db import Database

class GuestRepository():
    """
    Class for managing guests in the database.
    """

    def __init__(self):
        self.db = Database()

    async def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
    ) -> dict | None:
        query = """
            INSERT INTO guests (
                first_name, last_name, email, phone
            )
            VALUES ($1, $2, $3, $4)
            RETURNING *;
        """
        try:
            guest = await self.db.fetchrow(
                query, first_name, last_name, email, phone,
            )
            return guest
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="Guest with this email or phone already exists"
            )

    async def get_by_id(
        self,
        guest_id: int,
    ) -> dict | None:
        query = """
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                created_at
            FROM guests
            WHERE id = $1;
        """
        return await self.db.fetchrow(
            query,
            guest_id,
        )

    async def get_all(
        self,
    ) -> list[dict]:
        query = """
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                created_at
            FROM guests;
        """
        guests = await self.db.fetch(query)
        return [
            dict(guest)
            for guest in guests
        ]

    async def update(
        self,
        id: int,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        phone: str | None,
    ) -> dict | None:
        query = """
            UPDATE guests
            SET
                first_name = COALESCE($2, first_name),
                last_name = COALESCE($3, last_name),
                email = COALESCE($4, email),
                phone = COALESCE($5, phone)
            WHERE id = $1
            RETURNING *;
        """
        try:
            guest = await self.db.fetchrow(
                query, id, first_name, last_name, email, phone,
            )
            return guest
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="Guest with this email or phone already exists"
            )

    async def delete(
        self,
        id: int,
    ):
        query = """
            DELETE FROM guests
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(query, id)
