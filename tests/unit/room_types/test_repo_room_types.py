import pytest
import asyncpg

from app.exceptions.database import (
    RoomTypeAlreadyExistsError,
    RoomTypeInUseError,
)

"""
Repository -> raw SQL queries -> PostgreSQL
"""

@pytest.mark.asyncio
async def test_create_room_type(
    room_type_repository,
    room_type_data,
):
    room_type_repository.db.fetchrow.return_value = room_type_data

    result = await room_type_repository.create(
        room_type=room_type_data["room_type"],
    )

    assert result == room_type_data

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "INSERT INTO room_types" in query
    assert "VALUES ($1)" in query
    assert "RETURNING *" in query

    assert args == [
        room_type_data["room_type"],
    ]


@pytest.mark.asyncio
async def test_create_room_type_already_exists(
    room_type_repository,
):
    room_type_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.UniqueViolationError()
    )

    with pytest.raises(RoomTypeAlreadyExistsError):
        await room_type_repository.create(
            room_type="already_exists",
        )


@pytest.mark.asyncio
async def test_get_room_type_by_id(
    room_type_repository,
    room_type_data,
):
    room_type_repository.db.fetchrow.return_value = (
        room_type_data
    )

    result = await room_type_repository.get_by_id(
        room_type_data["id"]
    )

    assert result == room_type_data

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "SELECT" in query
    assert "FROM room_types" in query
    assert "WHERE id = $1" in query

    assert args == [room_type_data["id"]]


@pytest.mark.asyncio
async def test_get_room_type_by_id_not_found(
    room_type_repository,
):
    room_type_repository.db.fetchrow.return_value = None

    result = await room_type_repository.get_by_id(999)

    assert result is None

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "SELECT" in query
    assert "FROM room_types" in query
    assert "WHERE id = $1" in query

    assert args == [999]


@pytest.mark.asyncio
async def test_get_all_room_types(
    room_type_repository,
    room_type_data,
):
    room_type_repository.db.fetch.return_value = [
        room_type_data
    ]

    result = await room_type_repository.get_all()

    assert result == [room_type_data]

    room_type_repository.db.fetch.assert_awaited_once()

    query = room_type_repository.db.fetch.call_args.args[0]

    assert "SELECT" in query
    assert "FROM room_types" in query



@pytest.mark.asyncio
async def test_update_room_type(
    room_type_repository,
    room_type_data,
):
    updated_room_type = {
        **room_type_data,
        "room_type": "Updated",
    }

    room_type_repository.db.fetchrow.return_value = (
        updated_room_type
    )

    result = await room_type_repository.update(
        id=room_type_data["id"],
        room_type="Updated",
    )

    assert result == updated_room_type

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "UPDATE room_types" in query
    assert "COALESCE" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [
        room_type_data["id"],
        "Updated",
    ]


@pytest.mark.asyncio
async def test_update_room_type_not_found(
    room_type_repository,
):
    room_type_repository.db.fetchrow.return_value = None

    result = await room_type_repository.update(
        id=999,
        room_type="Updated",
    )

    assert result is None

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "UPDATE room_types" in query
    assert "WHERE id = $1" in query

    assert args == [
        999,
        "Updated",
    ]


@pytest.mark.asyncio
async def test_update_room_type_already_exists(
    room_type_repository,
):
    room_type_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.UniqueViolationError()
    )

    with pytest.raises(RoomTypeAlreadyExistsError):
        await room_type_repository.update(
            id=1,
            room_type="already_exists",
        )


@pytest.mark.asyncio
async def test_delete_room_type(
    room_type_repository,
    room_type_data,
):
    room_type_repository.db.fetchrow.return_value = (
        room_type_data
    )

    result = await room_type_repository.delete(
        id=room_type_data["id"]
    )

    assert result == room_type_data

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "DELETE FROM room_types" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [
        room_type_data["id"],
    ]


@pytest.mark.asyncio
async def test_delete_room_type_not_found(
    room_type_repository,
):
    room_type_repository.db.fetchrow.return_value = None

    result = await room_type_repository.delete(id=999)

    assert result is None

    room_type_repository.db.fetchrow.assert_awaited_once()

    query, *args = (
        room_type_repository.db.fetchrow.call_args.args
    )

    assert "DELETE FROM room_types" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [999]


@pytest.mark.asyncio
async def test_delete_room_type_in_use(
    room_type_repository,
):
    room_type_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.ForeignKeyViolationError()
    )

    with pytest.raises(RoomTypeInUseError):
        await room_type_repository.delete(id=1)
