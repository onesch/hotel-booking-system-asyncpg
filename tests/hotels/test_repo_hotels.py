import pytest

"""
Repository -> roper SQL Queries -> PostgreSQL
"""

@pytest.mark.asyncio
async def test_create_hotel(hotel_repository, hotel_data):
    hotel_repository.db.fetchrow.return_value = hotel_data

    result = await hotel_repository.create(
        name=hotel_data["name"],
        address=hotel_data["address"],
        description=hotel_data["description"],
        owner_id=hotel_data["owner_id"],
    )

    assert result == hotel_data

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "INSERT INTO hotels" in query
    assert "VALUES ($1, $2, $3, $4)" in query
    assert "RETURNING *" in query

    assert args == [
        hotel_data["name"],
        hotel_data["address"],
        hotel_data["description"],
        hotel_data["owner_id"],
    ]


@pytest.mark.asyncio
async def test_get_hotel_by_id(hotel_repository, hotel_data):
    hotel_repository.db.fetchrow.return_value = hotel_data

    result = await hotel_repository.get_by_id(hotel_data["id"])

    assert result == hotel_data

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM hotels" in query
    assert "WHERE id = $1" in query

    assert args == [hotel_data["id"]]


@pytest.mark.asyncio
async def test_get_hotel_by_id_not_found(hotel_repository):
    hotel_repository.db.fetchrow.return_value = None

    result = await hotel_repository.get_by_id(999)

    assert result is None

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "SELECT" in query
    assert "FROM hotels" in query
    assert "WHERE id = $1" in query

    assert args == [999]


@pytest.mark.asyncio
async def test_get_all_hotels(hotel_repository, hotel_data):
    hotel_repository.db.fetch.return_value = [hotel_data]

    result = await hotel_repository.get_all()

    assert result == [hotel_data]

    hotel_repository.db.fetch.assert_awaited_once()

    query = hotel_repository.db.fetch.call_args.args[0]

    assert "SELECT" in query
    assert "FROM hotels" in query


@pytest.mark.asyncio
async def test_update_hotel(hotel_repository, hotel_data):
    updated_hotel = {
        **hotel_data,
        "description": "Updated",
    }

    hotel_repository.db.fetchrow.return_value = updated_hotel

    result = await hotel_repository.update(
        id=hotel_data["id"],
        name=None,
        address=None,
        description="Updated",
    )

    assert result == updated_hotel

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "UPDATE hotels" in query
    assert "COALESCE" in query
    assert "RETURNING *" in query

    assert args == [
        hotel_data["id"],
        None,
        None,
        "Updated",
    ]


@pytest.mark.asyncio
async def test_update_hotel_not_found(hotel_repository):
    hotel_repository.db.fetchrow.return_value = None

    result = await hotel_repository.update(
        id=999,
        name=None,
        address=None,
        description="Not found",
    )

    assert result is None

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "UPDATE hotels" in query
    assert "WHERE id = $1" in query

    assert args == [
        999,
        None,
        None,
        "Not found",
    ]


@pytest.mark.asyncio
async def test_delete_hotel(hotel_repository, hotel_data):
    hotel_repository.db.fetchrow.return_value = hotel_data

    result = await hotel_repository.delete(id=hotel_data["id"])

    assert result == hotel_data

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "DELETE FROM hotels" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [hotel_data["id"]]


@pytest.mark.asyncio
async def test_delete_hotel_not_found(hotel_repository):
    hotel_repository.db.fetchrow.return_value = None

    result = await hotel_repository.delete(id=999)

    assert result is None

    hotel_repository.db.fetchrow.assert_awaited_once()

    query, *args = hotel_repository.db.fetchrow.call_args.args

    assert "DELETE FROM hotels" in query
    assert "WHERE id = $1" in query
    assert "RETURNING *" in query

    assert args == [999]
