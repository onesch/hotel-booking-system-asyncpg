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
        password_hash: str,
    ) -> dict | None:
        query = """
            INSERT INTO guests (
                first_name,
                last_name,
                email,
                phone,
                password_hash
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *;
        """
        try:
            guest = await self.db.fetchrow(
                query,
                first_name,
                last_name,
                email,
                phone,
                password_hash,
            )
            return guest
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="Guest with this email or phone already exists"
            )

    async def create_business(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password_hash: str,
    ) -> dict | None:
        query = """
            INSERT INTO guests (
                first_name,
                last_name,
                email,
                phone,
                password_hash,
                role
            )
            VALUES ($1, $2, $3, $4, $5, 'business')
            RETURNING *;
        """
        try:
            guest = await self.db.fetchrow(
                query,
                first_name,
                last_name,
                email,
                phone,
                password_hash,
            )
            return guest
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="Guest with this email or phone already exists",
            )

    async def get_by_id(self, id: int) -> dict | None:
        query = """
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                role,
                created_at
            FROM guests
            WHERE id = $1;
        """
        return await self.db.fetchrow(query, id)

    async def get_by_email(self, email: str) -> dict | None:
        return await self.db.fetchrow(
            """
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                role,
                created_at
            FROM guests
            WHERE email = $1
            """,
            email,
        )

    async def get_all(self) -> list[dict]:
        query = """
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone,
                role,
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
        password_hash=None,
    ) -> dict | None:
        query = """
            UPDATE guests
            SET
                first_name = COALESCE($2, first_name),
                last_name = COALESCE($3, last_name),
                email = COALESCE($4, email),
                phone = COALESCE($5, phone),
                password_hash = COALESCE($7, password_hash)
            WHERE id = $1
            RETURNING *;
        """
        try:
            guest = await self.db.fetchrow(
                query, id, first_name, last_name, email, phone, password_hash,
            )
            return guest
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="Guest with this email or phone already exists"
            )

    async def delete(self, id: int) -> dict | None:
        query = """
            DELETE FROM guests
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(query, id)
