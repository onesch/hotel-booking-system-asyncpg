import pytest
from fastapi import HTTPException

from app.schemas.hotels import (
    HotelCreate,
    HotelDelete,
    HotelUpdate,
)

"""
Service -> correctly calls the Repository
        -> correctly handles the Repository result
"""

@pytest.mark.asyncio
async def test_create_hotel(hotel_service, hotel_data):
    hotel_service.repo.create.return_value = hotel_data

    hotel = HotelCreate(
        name=hotel_data["name"],
        address=hotel_data["address"],
        description=hotel_data["description"],
    )

    result = await hotel_service.create(hotel)

    assert result == hotel_data

    hotel_service.repo.create.assert_awaited_once_with(
        name=hotel_data["name"],
        address=hotel_data["address"],
        description=hotel_data["description"],
    )


@pytest.mark.asyncio
async def test_get_hotel_by_id(hotel_service, hotel_data):
    hotel_service.repo.get_by_id.return_value = hotel_data

    result = await hotel_service.get_by_id(hotel_data["id"])

    assert result == hotel_data

    hotel_service.repo.get_by_id.assert_awaited_once_with(hotel_data["id"])


@pytest.mark.asyncio
async def test_get_hotel_by_id_not_found(hotel_service):
    hotel_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await hotel_service.get_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel not found"

    hotel_service.repo.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_hotels(hotel_service, hotel_data):
    hotel_service.repo.get_all.return_value = [hotel_data]

    result = await hotel_service.get_all()

    assert result == [hotel_data]

    hotel_service.repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_hotel(hotel_service, hotel_data):
    updated_hotel = {
        **hotel_data,
        "description": "Updated",
    }

    hotel_service.repo.update.return_value = updated_hotel

    hotel = HotelUpdate(
        id=updated_hotel["id"],
        name=None,
        address=None,
        description="Updated",
    )

    result = await hotel_service.update(hotel)

    assert result == updated_hotel

    hotel_service.repo.update.assert_awaited_once_with(
        id=updated_hotel["id"],
        name=None,
        address=None,
        description="Updated",
    )


@pytest.mark.asyncio
async def test_update_hotel_not_found(hotel_service):
    hotel_service.repo.update.return_value = None

    hotel = HotelUpdate(
        id=999,
        name=None,
        address=None,
        description="Not found",
    )

    with pytest.raises(HTTPException) as exc:
        await hotel_service.update(hotel)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel not found"

    hotel_service.repo.update.assert_awaited_once_with(
        id=999,
        name=None,
        address=None,
        description="Not found",
    )


@pytest.mark.asyncio
async def test_delete_hotel(hotel_service, hotel_data):
    hotel_service.repo.delete.return_value = hotel_data

    hotel = HotelDelete(id=hotel_data["id"])

    result = await hotel_service.delete(hotel)

    assert result == hotel_data

    hotel_service.repo.delete.assert_awaited_once_with(id=hotel_data["id"])


@pytest.mark.asyncio
async def test_delete_hotel_not_found(hotel_service):
    hotel_service.repo.delete.return_value = None

    hotel = HotelDelete(id=999)

    with pytest.raises(HTTPException) as exc:
        await hotel_service.delete(hotel)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel not found"

    hotel_service.repo.delete.assert_awaited_once_with(id=999)
