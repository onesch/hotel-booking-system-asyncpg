import asyncpg
from typing import Any

from app.settings import DATABASE_URL


class Database:
    """
    Database connection manager for PostgreSQL.

    Provides methods for creating database connections,
    executing SQL queries, and fetching query results using asyncpg.
    """

    def __init__(self):
        self.database_url = DATABASE_URL

        if not self.database_url:
            raise ValueError("DATABASE_URL is not set")

    async def get_connection(self) -> asyncpg.Connection:
        """
        Create and return a new PostgreSQL database connection.
        """
        try:
            conn = await asyncpg.connect(self.database_url)

            print("Connection is alive.")

            version = await conn.fetchval("SELECT version();")
            print(version)

            return conn

        except asyncpg.exceptions.ClientConfigurationError as e:
            print(f"Error connecting to the database: {e}")
            raise

    async def close_connection(
        self,
        conn: asyncpg.Connection,
    ) -> None:
        """
        Close an active database connection.
        """
        await conn.close()
        print("Connection closed.")

    async def fetch(
        self,
        query: str,
        *args,
    ) -> list[dict[str, Any]]:
        """
        Execute SELECT query and return multiple rows.
        """
        conn = await self.get_connection()

        try:
            result = await conn.fetch(query, *args)
            return [
                dict(row)
                for row in result
            ]

        finally:
            await self.close_connection(conn)

    async def execute(
        self,
        query: str,
        *args,
    ) -> None:
        """
        Execute SQL query without returning data.

        Used for queries where result rows are not required,
        such as INSERT, UPDATE, or DELETE without RETURNING.
        """
        conn = await self.get_connection()

        try:
            await conn.execute(query, *args)

        finally:
            await self.close_connection(conn)

    async def fetchrow(
        self,
        query: str,
        *args,
    ) -> dict | None:
        """
        Execute SQL query and return a single row.

        Usually used with queries containing RETURNING clause.
        """
        conn = await self.get_connection()

        try:
            result = await conn.fetchrow(query, *args)

            return dict(result) if result else None

        finally:
            await self.close_connection(conn)
