import asyncpg
import pytest

from app.exceptions.database import RelatedEntityNotFoundError


"""
Repository -> proper SQL queries -> PostgreSQL
"""


@pytest.mark.asyncio
async def test_create_room(room_repository, room_data):
    room_repository.db.fetchrow.return_value = room_data

    result = await room_repository.create(
        room_number=room_data["room_number"],
        room_floor=room_data["room_floor"],
        is_active=room_data["is_active"],
        hotel_id=room_data["hotel_id"],
        room_type_id=room_data["room_type_id"],
    )

    assert result == room_data
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "INSERT INTO rooms" in query
    assert "VALUES ($1, $2, $3, $4, $5)" in query
    assert "RETURNING *" in query
    assert args == [
        room_data["room_number"],
        room_data["room_floor"],
        room_data["is_active"],
        room_data["hotel_id"],
        room_data["room_type_id"],
    ]


@pytest.mark.asyncio
async def test_create_room_with_missing_related_entity(room_repository, room_data):
    room_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.ForeignKeyViolationError()
    )

    with pytest.raises(RelatedEntityNotFoundError):
        await room_repository.create(
            room_number=room_data["room_number"],
            room_floor=room_data["room_floor"],
            is_active=room_data["is_active"],
            hotel_id=room_data["hotel_id"],
            room_type_id=room_data["room_type_id"],
        )

    room_repository.db.fetchrow.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_room_by_id(room_repository, room_data):
    room_repository.db.fetchrow.return_value = room_data

    result = await room_repository.get_by_id(room_data["id"])

    assert result == room_data
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM rooms" in query
    assert "WHERE id = $1" in query
    assert args == [room_data["id"]]


@pytest.mark.asyncio
async def test_get_room_by_id_not_found(room_repository):
    room_repository.db.fetchrow.return_value = None

    result = await room_repository.get_by_id(999)

    assert result is None
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM rooms" in query
    assert "WHERE id = $1" in query
    assert args == [999]


@pytest.mark.asyncio
async def test_get_all_rooms(room_repository, room_data):
    room_repository.db.fetch.return_value = [room_data]

    result = await room_repository.get_all()

    assert result == [room_data]
    room_repository.db.fetch.assert_awaited_once()

    query = room_repository.db.fetch.call_args.args[0]

    assert "SELECT" in query
    assert "FROM rooms" in query


@pytest.mark.asyncio
async def test_update_room(room_repository, room_data):
    updated_room = {
        **room_data,
        "room_number": "202",
        "is_active": False,
    }
    room_repository.db.fetchrow.return_value = updated_room

    result = await room_repository.update(
        id=room_data["id"],
        room_number="202",
        room_floor=None,
        is_active=False,
        hotel_id=None,
        room_type_id=None,
    )

    assert result == updated_room
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "UPDATE rooms" in query
    assert "COALESCE" in query
    assert "RETURNING *" in query
    assert args == [
        room_data["id"],
        "202",
        None,
        False,
        None,
        None,
    ]


@pytest.mark.asyncio
async def test_update_room_not_found(room_repository):
    room_repository.db.fetchrow.return_value = None

    result = await room_repository.update(
        id=999,
        room_number="999",
        room_floor=None,
        is_active=None,
        hotel_id=None,
        room_type_id=None,
    )

    assert result is None
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "UPDATE rooms" in query
    assert "WHERE id = $1" in query
    assert args == [
        999,
        "999",
        None,
        None,
        None,
        None,
    ]


@pytest.mark.asyncio
async def test_update_room_with_missing_related_entity(room_repository, room_data):
    room_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.ForeignKeyViolationError()
    )

    with pytest.raises(RelatedEntityNotFoundError):
        await room_repository.update(
            id=room_data["id"],
            room_number=None,
            room_floor=None,
            is_active=None,
            hotel_id=999,
            room_type_id=None,
        )

    room_repository.db.fetchrow.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_room(room_repository, room_data):
    room_repository.db.fetchrow.return_value = room_data

    result = await room_repository.delete(id=room_data["id"])

    assert result == room_data
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "DELETE FROM rooms" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query
    assert args == [room_data["id"]]


@pytest.mark.asyncio
async def test_delete_room_not_found(room_repository):
    room_repository.db.fetchrow.return_value = None

    result = await room_repository.delete(id=999)

    assert result is None
    room_repository.db.fetchrow.assert_awaited_once()

    query, *args = room_repository.db.fetchrow.call_args.args

    assert "DELETE FROM rooms" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query
    assert args == [999]
