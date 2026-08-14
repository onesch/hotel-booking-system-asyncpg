import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import HTTPException

from app.main import app

"""
HTTP request -> Router -> mock GuestService
"""


@pytest.mark.asyncio
async def test_get_guest_by_id(api_guest_service, guest_data, monkeypatch):
    guest = {
        **guest_data,
        "role": "user",
        "created_at": "2026-08-05T12:00:00",
    }

    api_guest_service.get_by_id.return_value = guest

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get(
            f"/guests/{guest['id']}"
        )

    assert response.status_code == 200
    assert response.json() == guest

    api_guest_service.get_by_id.assert_awaited_once_with(guest_data["id"])


@pytest.mark.asyncio
async def test_get_guest_by_id_not_found(api_guest_service, monkeypatch):
    api_guest_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Guest not found",
    )

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/guests/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Guest not found"}

    api_guest_service.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_guests(api_guest_service, guest_data, monkeypatch):
    guest = {
        **guest_data,
        "role": "user",
        "created_at": "2026-08-05T12:00:00",
    }

    api_guest_service.get_all.return_value = [guest]

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/guests/")

    assert response.status_code == 200
    assert response.json() == [guest]

    api_guest_service.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_guest(api_guest_service, guest_data, monkeypatch):
    updated_guest = {
        **guest_data,
        "first_name": "Updated",
    }

    api_guest_service.update.return_value = updated_guest

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    payload = {
        "id": guest_data["id"],
        "first_name": "Updated",
        "last_name": None,
        "email": None,
        "phone": None,
        "role": None,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/guests/update",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == updated_guest

    api_guest_service.update.assert_awaited_once()

    guest = api_guest_service.update.call_args.args[0]

    assert guest.id == guest_data["id"]
    assert guest.first_name == "Updated"
    assert guest.last_name is None
    assert guest.email is None
    assert guest.phone is None
    assert guest.role is None


@pytest.mark.asyncio
async def test_update_guest_not_found(api_guest_service, monkeypatch):
    api_guest_service.update.side_effect = HTTPException(
        status_code=404,
        detail="Guest not found",
    )

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    payload = {
        "id": 999,
        "first_name": "Updated",
        "last_name": None,
        "email": None,
        "phone": None,
        "role": None,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/guests/update",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Guest not found"
    }

    api_guest_service.update.assert_awaited_once()

    guest = api_guest_service.update.call_args.args[0]

    assert guest.id == 999
    assert guest.first_name == "Updated"


@pytest.mark.asyncio
async def test_delete_guest(api_guest_service, guest_data, monkeypatch):
    api_guest_service.delete.return_value = guest_data

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
    )

    payload = {
        "id": guest_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.request(
            "DELETE",
            "/guests/delete",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == guest_data

    api_guest_service.delete.assert_awaited_once()

    guest = api_guest_service.delete.call_args.args[0]

    assert guest.id == guest_data["id"]


@pytest.mark.asyncio
async def test_delete_guest_not_found(api_guest_service, monkeypatch):
    api_guest_service.delete.side_effect = HTTPException(
        status_code=404,
        detail="Guest not found",
    )

    monkeypatch.setattr(
        "app.routers.guests.guests_service",
        api_guest_service,
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
            "/guests/delete",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Guest not found"
    }

    api_guest_service.delete.assert_awaited_once()

    guest = api_guest_service.delete.call_args.args[0]

    assert guest.id == 999
