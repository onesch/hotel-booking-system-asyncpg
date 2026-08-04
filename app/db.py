import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise ValueError("DATABASE_URL is not set")

    async def get_connection(self) -> asyncpg.Connection:
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
        await conn.close()
        print("Connection closed.")

    async def fetch(
        self,
        query: str,
        *args,
    ) -> list[asyncpg.Record]:
        conn = await self.get_connection()

        try:
            result = await conn.fetch(query, *args)
            return result

        finally:
            await self.close_connection(conn)

    async def execute(
        self,
        query: str,
        *args,
    ) -> None:
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
        conn = await self.get_connection()

        try:
            result = await conn.fetchrow(query, *args)

            return dict(result) if result else None

        finally:
            await self.close_connection(conn)
