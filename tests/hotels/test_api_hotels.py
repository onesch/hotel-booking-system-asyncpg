import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import HTTPException

from app.main import app

"""
HTTP request -> Router -> mock HotelService
"""

@pytest.mark.asyncio
async def test_create_hotel(api_hotel_service, hotel_data, monkeypatch):
    api_hotel_service.create.return_value = hotel_data

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    payload = {
        "name": hotel_data["name"],
        "address": hotel_data["address"],
        "description": hotel_data["description"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.post(
            "/hotels/create",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == hotel_data

    api_hotel_service.create.assert_awaited_once()

    hotel = api_hotel_service.create.call_args.args[0]

    assert hotel.name == hotel_data["name"]
    assert hotel.address == hotel_data["address"]
    assert hotel.description == hotel_data["description"]


@pytest.mark.asyncio
async def test_get_hotel_by_id(api_hotel_service, hotel_data, monkeypatch):
    hotel = {
        **hotel_data,
        "created_at": "2026-08-05T12:00:00",
    }

    api_hotel_service.get_by_id.return_value = hotel

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get(f"/hotels/{hotel['id']}")

    assert response.status_code == 200
    assert response.json() == hotel

    api_hotel_service.get_by_id.assert_awaited_once_with(hotel_data["id"])


@pytest.mark.asyncio
async def test_get_hotel_by_id_not_found(api_hotel_service, monkeypatch):
    api_hotel_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Hotel not found",
    )

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/hotels/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Hotel not found"}

    api_hotel_service.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_hotels(api_hotel_service, hotel_data, monkeypatch):
    hotel = {
        **hotel_data,
        "created_at": "2026-08-05T12:00:00",
    }

    api_hotel_service.get_all.return_value = [hotel]

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/hotels/")

    assert response.status_code == 200
    assert response.json() == [hotel]

    api_hotel_service.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_hotel(api_hotel_service, hotel_data, monkeypatch):
    updated_hotel = {
        **hotel_data,
        "description": "Updated",
    }

    api_hotel_service.update.return_value = updated_hotel

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    payload = {
        "id": hotel_data["id"],
        "name": None,
        "address": None,
        "description": "Updated",
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/hotels/update",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == updated_hotel

    api_hotel_service.update.assert_awaited_once()

    hotel = api_hotel_service.update.call_args.args[0]

    assert hotel.id == hotel_data["id"]
    assert hotel.name is None
    assert hotel.address is None
    assert hotel.description == "Updated"


@pytest.mark.asyncio
async def test_update_hotel_not_found(api_hotel_service, monkeypatch):
    api_hotel_service.update.side_effect = HTTPException(
        status_code=404,
        detail="Hotel not found",
    )

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    payload = {
        "id": 999,
        "name": None,
        "address": None,
        "description": "Not found",
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/hotels/update",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Hotel not found"}

    api_hotel_service.update.assert_awaited_once()

    hotel = api_hotel_service.update.call_args.args[0]

    assert hotel.id == 999
    assert hotel.description == "Not found"


@pytest.mark.asyncio
async def test_delete_hotel(api_hotel_service, hotel_data, monkeypatch):
    api_hotel_service.delete.return_value = hotel_data

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    payload = {
        "id": hotel_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.request(
            "DELETE",
            "/hotels/delete",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == hotel_data

    api_hotel_service.delete.assert_awaited_once()

    hotel = api_hotel_service.delete.call_args.args[0]

    assert hotel.id == hotel_data["id"]


@pytest.mark.asyncio
async def test_delete_hotel_not_found(api_hotel_service, monkeypatch):
    api_hotel_service.delete.side_effect = HTTPException(
        status_code=404,
        detail="Hotel not found",
    )

    monkeypatch.setattr(
        "app.routers.hotels.hotels_service",
        api_hotel_service,
    )

    payload = {
        "id": 999,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.request(
            "DELETE",
            "/hotels/delete",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Hotel not found"}

    api_hotel_service.delete.assert_awaited_once()

    hotel = api_hotel_service.delete.call_args.args[0]

    assert hotel.id == 999
