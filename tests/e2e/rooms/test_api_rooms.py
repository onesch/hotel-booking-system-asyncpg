import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.main import app


"""
HTTP request -> Router -> mock RoomService
"""


@pytest.mark.asyncio
async def test_create_room(
    api_room_service,
    room_data,
    override_business_guest,
    monkeypatch,
):
    api_room_service.create.return_value = room_data
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )
    payload = {
        "room_number": room_data["room_number"],
        "room_floor": room_data["room_floor"],
        "is_active": room_data["is_active"],
        "hotel_id": room_data["hotel_id"],
        "room_type_id": room_data["room_type_id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/rooms/create",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == room_data
    api_room_service.create.assert_awaited_once()

    room = api_room_service.create.call_args.args[0]

    assert room.room_number == room_data["room_number"]
    assert room.room_floor == room_data["room_floor"]
    assert room.is_active == room_data["is_active"]
    assert room.hotel_id == room_data["hotel_id"]
    assert room.room_type_id == room_data["room_type_id"]


@pytest.mark.asyncio
async def test_create_room_with_missing_related_entity(
    api_room_service,
    room_data,
    override_business_guest,
    monkeypatch,
):
    api_room_service.create.side_effect = HTTPException(
        status_code=404,
        detail="Hotel or room type not found",
    )
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )
    payload = {
        "room_number": room_data["room_number"],
        "room_floor": room_data["room_floor"],
        "is_active": room_data["is_active"],
        "hotel_id": 999,
        "room_type_id": room_data["room_type_id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/rooms/create",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Hotel or room type not found",
    }
    api_room_service.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_room_by_id(api_room_service, room_data, monkeypatch):
    api_room_service.get_by_id.return_value = room_data
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get(f"/rooms/{room_data['id']}")

    assert response.status_code == 200
    assert response.json() == room_data
    api_room_service.get_by_id.assert_awaited_once_with(room_data["id"])


@pytest.mark.asyncio
async def test_get_room_by_id_not_found(api_room_service, monkeypatch):
    api_room_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Room not found",
    )
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/rooms/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
    api_room_service.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_rooms(api_room_service, room_data, monkeypatch):
    api_room_service.get_all.return_value = [room_data]
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/rooms/")

    assert response.status_code == 200
    assert response.json() == [room_data]
    api_room_service.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_room(
    api_room_service,
    room_data,
    override_business_guest,
    monkeypatch,
):
    updated_room = {
        **room_data,
        "room_number": "202",
        "is_active": False,
    }
    api_room_service.update.return_value = updated_room
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )
    payload = {
        "id": room_data["id"],
        "room_number": "202",
        "room_floor": None,
        "is_active": False,
        "hotel_id": None,
        "room_type_id": None,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.patch(
            "/rooms/update",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == updated_room
    api_room_service.update.assert_awaited_once()

    room = api_room_service.update.call_args.args[0]

    assert room.id == room_data["id"]
    assert room.room_number == "202"
    assert room.room_floor is None
    assert room.is_active is False
    assert room.hotel_id is None
    assert room.room_type_id is None


@pytest.mark.asyncio
async def test_update_room_not_found(
    api_room_service,
    override_business_guest,
    monkeypatch,
):
    api_room_service.update.side_effect = HTTPException(
        status_code=404,
        detail="Room not found",
    )
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )
    payload = {
        "id": 999,
        "room_number": "999",
        "room_floor": None,
        "is_active": None,
        "hotel_id": None,
        "room_type_id": None,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.patch(
            "/rooms/update",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
    api_room_service.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_room(
    api_room_service,
    room_data,
    override_business_guest,
    monkeypatch,
):
    api_room_service.delete.return_value = room_data
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
    )
    payload = {
        "id": room_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.request(
            "DELETE",
            "/rooms/delete",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == room_data
    api_room_service.delete.assert_awaited_once()

    room = api_room_service.delete.call_args.args[0]

    assert room.id == room_data["id"]


@pytest.mark.asyncio
async def test_delete_room_not_found(
    api_room_service,
    override_business_guest,
    monkeypatch,
):
    api_room_service.delete.side_effect = HTTPException(
        status_code=404,
        detail="Room not found",
    )
    monkeypatch.setattr(
        "app.routers.rooms.rooms_service",
        api_room_service,
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
            "/rooms/delete",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}
    api_room_service.delete.assert_awaited_once()
