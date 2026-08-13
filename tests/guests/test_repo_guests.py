import pytest

"""
Repository -> roper SQL Queries -> PostgreSQL
"""

@pytest.mark.asyncio
async def test_create_guest(guest_repository, guest_data):
    guest_repository.db.fetchrow.return_value = guest_data

    result = await guest_repository.create(
        first_name=guest_data["first_name"],
        last_name=guest_data["last_name"],
        email=guest_data["email"],
        phone=guest_data["phone"],
    )

    assert result == guest_data

    guest_repository.db.fetchrow.assert_awaited_once()

    query, *args = guest_repository.db.fetchrow.call_args.args

    assert "INSERT INTO guests" in query
    assert "VALUES ($1, $2, $3, $4)" in query
    assert "RETURNING *" in query

    assert args == [
        guest_data["first_name"],
        guest_data["last_name"],
        guest_data["email"],
        guest_data["phone"],
    ]


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
