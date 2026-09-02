import asyncpg
import pytest_asyncio

from app.settings import TEST_DATABASE_URL


@pytest_asyncio.fixture
async def test_db():
    conn = await asyncpg.connect(TEST_DATABASE_URL)

    try:
        yield conn
    finally:
        await conn.close()


@pytest_asyncio.fixture
async def clean_database(test_db):
    await test_db.execute("""
        TRUNCATE TABLE
            bookings,
            rooms,
            hotels,
            room_types,
            guests
        RESTART IDENTITY CASCADE
    """)

    yield


@pytest_asyncio.fixture
async def guest(test_db):
    return await test_db.fetchrow("""
        INSERT INTO guests (
            first_name,
            last_name,
            email,
            phone,
            password_hash
        )
        VALUES (
            'Test',
            'User',
            'test@example.com',
            '+79990000000',
            'test_hash'
        )
        RETURNING *;
    """)


@pytest_asyncio.fixture
async def second_guest(test_db):
    return await test_db.fetchrow("""
        INSERT INTO guests (
            first_name,
            last_name,
            email,
            phone,
            password_hash
        )
        VALUES (
            'Second',
            'User',
            'second@example.com',
            '+79990000001',
            'test_hash'
        )
        RETURNING *;
    """)


@pytest_asyncio.fixture
async def hotel(test_db, guest):
    return await test_db.fetchrow("""
        INSERT INTO hotels (
            name,
            address,
            description,
            owner_id
        )
        VALUES (
            'Test Hotel',
            'Test Address',
            'Test Description',
            $1
        )
        RETURNING *;
    """, guest["id"])


@pytest_asyncio.fixture
async def room_type(test_db):
    return await test_db.fetchrow("""
        INSERT INTO room_types (room_type)
        VALUES ('Single')
        RETURNING *;
    """)


@pytest_asyncio.fixture
async def room(test_db, hotel, room_type):
    return await test_db.fetchrow("""
        INSERT INTO rooms (
            room_number,
            room_floor,
            is_active,
            hotel_id,
            room_type_id
        )
        VALUES (
            '101',
            '1',
            TRUE,
            $1,
            $2
        )
        RETURNING *;
    """, hotel["id"], room_type["id"])
