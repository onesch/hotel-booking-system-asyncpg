import asyncpg
from fastapi import HTTPException

from app.db import Database

class Guests():
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
