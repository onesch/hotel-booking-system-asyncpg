import asyncpg
from fastapi import HTTPException
import pytest

"""
Repository -> roper SQL Queries -> PostgreSQL
"""

@pytest.mark.asyncio
async def test_create_guest(guest_repository, guest_data):
    created_guest = {
        **guest_data,
        "password_hash": "hashed_password",
    }
    guest_repository.db.fetchrow.return_value = created_guest

    result = await guest_repository.create(
        first_name=created_guest["first_name"],
        last_name=created_guest["last_name"],
        email=created_guest["email"],
        phone=created_guest["phone"],
        password_hash=created_guest["password_hash"],
    )

    assert result == created_guest

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "INSERT INTO guests" in query
    assert "VALUES ($1, $2, $3, $4, $5)" in query
    assert "RETURNING *" in query

    assert args == [
        created_guest["first_name"],
        created_guest["last_name"],
        created_guest["email"],
        created_guest["phone"],
        created_guest["password_hash"],
    ]


@pytest.mark.asyncio
async def test_create_guest_duplicate(guest_repository):
    guest_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.UniqueViolationError()
    )

    with pytest.raises(HTTPException) as exc_info:
        await guest_repository.create(
            first_name="Name",
            last_name="LastName",
            email="example@email.com",
            phone="123456789",
            password_hash="hashed_password",
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == (
        "Guest with this email or phone already exists"
    )


@pytest.mark.asyncio
async def test_create_business_guest(guest_repository, guest_data):
    created_guest = {
        **guest_data,
        "password_hash": "hashed_password",
        "role": "business",
    }

    guest_repository.db.fetchrow.return_value = created_guest

    result = await guest_repository.create_business(
        first_name=created_guest["first_name"],
        last_name=created_guest["last_name"],
        email=created_guest["email"],
        phone=created_guest["phone"],
        password_hash=created_guest["password_hash"],
    )

    assert result == created_guest

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "INSERT INTO guests" in query
    assert "VALUES ($1, $2, $3, $4, $5, 'business')" in query
    assert "RETURNING *" in query

    assert args == [
        created_guest["first_name"],
        created_guest["last_name"],
        created_guest["email"],
        created_guest["phone"],
        created_guest["password_hash"],
    ]


@pytest.mark.asyncio
async def test_create_business_guest_duplicate(
    guest_repository,
    guest_data,
):
    guest_repository.db.fetchrow.side_effect = (
        asyncpg.exceptions.UniqueViolationError()
    )

    with pytest.raises(HTTPException) as exc:
        await guest_repository.create_business(
            first_name=guest_data["first_name"],
            last_name=guest_data["last_name"],
            email=guest_data["email"],
            phone=guest_data["phone"],
            password_hash="hashed_password",
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Guest with this email or phone already exists"
    )


@pytest.mark.asyncio
async def test_get_guest_by_id(guest_repository, guest_data):
    guest_repository.db.fetchrow.return_value = guest_data

    result = await guest_repository.get_by_id(guest_data["id"])

    assert result == guest_data

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM guests" in query
    assert "WHERE id = $1" in query

    assert args == [guest_data["id"]]


@pytest.mark.asyncio
async def test_get_guest_by_id_not_found(guest_repository):
    guest_repository.db.fetchrow.return_value = None

    result = await guest_repository.get_by_id(999)

    assert result is None

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM guests" in query
    assert "WHERE id = $1" in query

    assert args == [999]


@pytest.mark.asyncio
async def test_get_guest_by_email(guest_repository, guest_data):
    guest_repository.db.fetchrow.return_value = guest_data

    result = await guest_repository.get_by_email(
        guest_data["email"]
    )

    assert result == guest_data

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM guests" in query
    assert "WHERE email = $1" in query

    assert args == [guest_data["email"]]


@pytest.mark.asyncio
async def test_get_guest_by_email_not_found(guest_repository):
    guest_repository.db.fetchrow.return_value = None

    result = await guest_repository.get_by_email(
        "notfound@example.com"
    )

    assert result is None

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM guests" in query
    assert "WHERE email = $1" in query

    assert args == ["notfound@example.com"]


@pytest.mark.asyncio
async def test_get_all_guests(guest_repository, guest_data):
    guest_repository.db.fetch.return_value = [guest_data]

    result = await guest_repository.get_all()

    assert result == [guest_data]

    guest_repository.db.fetch.assert_awaited_once()

    query = guest_repository.db.fetch.call_args.args[0]

    assert "SELECT" in query
    assert "FROM guests" in query


@pytest.mark.asyncio
async def test_update_guest(guest_repository, guest_data):
    updated_guest = {
        **guest_data,
        "first_name": "Updated",
    }

    guest_repository.db.fetchrow.return_value = updated_guest

    result = await guest_repository.update(
        id=guest_data["id"],
        first_name="Updated",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )

    assert result == updated_guest

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "UPDATE guests" in query
    assert "COALESCE" in query
    assert "RETURNING *" in query

    assert args == [
        guest_data["id"],
        "Updated",
        None,
        None,
        None,
        None,
        None,
    ]


@pytest.mark.asyncio
async def test_update_guest_not_found(guest_repository):
    guest_repository.db.fetchrow.return_value = None

    result = await guest_repository.update(
        id=999,
        first_name="Name",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )

    assert result is None

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "UPDATE guests" in query
    assert "WHERE id = $1" in query

    assert args == [
        999,
        "Name",
        None,
        None,
        None,
        None,
        None,
    ]


@pytest.mark.asyncio
async def test_delete_guest(guest_repository, guest_data):
    guest_repository.db.fetchrow.return_value = guest_data

    result = await guest_repository.delete(id=guest_data["id"])

    assert result == guest_data

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "DELETE FROM guests" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [guest_data["id"]]


@pytest.mark.asyncio
async def test_delete_guest_not_found(guest_repository):
    guest_repository.db.fetchrow.return_value = None

    result = await guest_repository.delete(id=999)

    assert result is None

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "DELETE FROM guests" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [999]
