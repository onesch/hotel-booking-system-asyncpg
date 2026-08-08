from app.db import Database


class HotelRepository():
    """
    Class for managing hotels in the databse.
    """

    def __init__(self):
        self.db = Database()

    async def create(
        self,
        name: str,
        address: str,
        description: str | None,
    ) -> dict | None:
        query = """
            INSERT INTO hotels (
                name,
                address,
                description
            )
            VALUES ($1, $2, $3)
            RETURNING *;
        """
        return await self.db.fetchrow(
            query,
            name,
            address,
            description,
        )

    async def get_by_id(
        self,
        hotel_id: int,
    ) -> dict | None:
        query = """
            SELECT
                id,
                name,
                address,
                description,
                created_at
            FROM hotels
            WHERE id = $1;
        """
        return await self.db.fetchrow(
            query,
            hotel_id,
        )

    async def get_all(
        self,
    ) -> list[dict]:
        query = """
            SELECT
                id,
                name,
                address,
                description,
                created_at
            FROM hotels;
        """
        return await self.db.fetch(query)

    async def update(
        self,
        id: int,
        name: str | None,
        address: str | None,
        description: str | None,
    ) -> dict | None:
        query = """
            UPDATE hotels
            SET
                name = COALESCE($2, name),
                address = COALESCE($3, address),
                description = COALESCE($4, description)
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(
            query, id, name, address, description,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        query = """
            DELETE FROM hotels
            WHERE id = $1
            RETURNING *;
        """
        return await self.db.fetchrow(query, id)
