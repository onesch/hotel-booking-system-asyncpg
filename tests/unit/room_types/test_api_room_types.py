import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.main import app


"""
HTTP request -> Router -> mock RoomTypeService
"""

@pytest.mark.asyncio
async def test_create_room_type(
    api_room_type_service,
    room_type_data,
    override_admin_guest,
    monkeypatch,
):
    api_room_type_service.create.return_value = room_type_data

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    payload = {
        "room_type": room_type_data["room_type"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.post(
            "/room-types/create",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == room_type_data

    api_room_type_service.create.assert_awaited_once()

    room_type = (
        api_room_type_service.create
        .call_args.args[0]
    )

    assert room_type.room_type == room_type_data["room_type"]


@pytest.mark.asyncio
async def test_get_room_type_by_id(
    api_room_type_service,
    room_type_data,
    monkeypatch,
):
    api_room_type_service.get_by_id.return_value = room_type_data

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get(
            f"/room-types/{room_type_data['id']}"
        )

    assert response.status_code == 200
    assert response.json() == room_type_data

    api_room_type_service.get_by_id.assert_awaited_once_with(
        room_type_data["id"]
    )


@pytest.mark.asyncio
async def test_get_room_type_by_id_not_found(
    api_room_type_service,
    monkeypatch,
):
    api_room_type_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Room type not found",
    )

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/room-types/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Room type not found"
    }

    api_room_type_service.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_room_types(
    api_room_type_service,
    room_type_data,
    monkeypatch,
):
    api_room_type_service.get_all.return_value = [
        room_type_data
    ]

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/room-types/")

    assert response.status_code == 200
    assert response.json() == [room_type_data]

    api_room_type_service.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_room_type(
    api_room_type_service,
    room_type_data,
    override_admin_guest,
    monkeypatch,
):
    updated_room_type = {
        **room_type_data,
        "room_type": "Updated",
    }

    api_room_type_service.update.return_value = (
        updated_room_type
    )

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    payload = {
        "id": room_type_data["id"],
        "room_type": "Updated",
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.patch(
            "/room-types/update",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == updated_room_type

    api_room_type_service.update.assert_awaited_once()

    room_type = (
        api_room_type_service.update
        .call_args.args[0]
    )

    assert room_type.id == room_type_data["id"]
    assert room_type.room_type == "Updated"


@pytest.mark.asyncio
async def test_update_room_type_not_found(
    api_room_type_service,
    override_admin_guest,
    monkeypatch,
):
    api_room_type_service.update.side_effect = HTTPException(
        status_code=404,
        detail="Room type not found",
    )

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    payload = {
        "id": 999,
        "room_type": "Updated",
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.patch(
            "/room-types/update",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Room type not found"
    }

    api_room_type_service.update.assert_awaited_once()

    room_type = (
        api_room_type_service.update
        .call_args.args[0]
    )

    assert room_type.id == 999
    assert room_type.room_type == "Updated"


@pytest.mark.asyncio
async def test_delete_room_type(
    api_room_type_service,
    room_type_data,
    override_admin_guest,
    monkeypatch,
):
    api_room_type_service.delete.return_value = room_type_data

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    payload = {
        "id": room_type_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.request(
            "DELETE",
            "/room-types/delete",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == room_type_data

    api_room_type_service.delete.assert_awaited_once()

    room_type = (
        api_room_type_service.delete
        .call_args.args[0]
    )

    assert room_type.id == room_type_data["id"]


@pytest.mark.asyncio
async def test_delete_room_type_not_found(
    api_room_type_service,
    override_admin_guest,
    monkeypatch,
):
    api_room_type_service.delete.side_effect = HTTPException(
        status_code=404,
        detail="Room type not found",
    )

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
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
            "/room-types/delete",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Room type not found"
    }

    api_room_type_service.delete.assert_awaited_once()

    room_type = (
        api_room_type_service.delete
        .call_args.args[0]
    )

    assert room_type.id == 999


@pytest.mark.asyncio
async def test_delete_room_type_in_use(
    api_room_type_service,
    override_admin_guest,
    monkeypatch,
):
    api_room_type_service.delete.side_effect = HTTPException(
        status_code=409,
        detail="Room type is used by one or more rooms",
    )

    monkeypatch.setattr(
        "app.routers.room_types.room_types_service",
        api_room_type_service,
    )

    payload = {
        "id": 1,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.request(
            "DELETE",
            "/room-types/delete",
            json=payload,
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Room type is used by one or more rooms"
    }

    api_room_type_service.delete.assert_awaited_once()

    room_type = (
        api_room_type_service.delete
        .call_args.args[0]
    )

    assert room_type.id == 1
