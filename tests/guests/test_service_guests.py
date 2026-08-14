import pytest
from fastapi import HTTPException

from app.schemas.guests import (
    GuestDelete,
    GuestUpdate,
)

"""
Service -> correctly calls the Repository
        -> correctly handles the Repository result
"""


@pytest.mark.asyncio
async def test_get_guest_by_id(guest_service, guest_data):
    guest_service.repo.get_by_id.return_value = guest_data

    result = await guest_service.get_by_id(guest_data["id"])

    assert result == guest_data

    guest_service.repo.get_by_id.assert_awaited_once_with(guest_data["id"])


@pytest.mark.asyncio
async def test_get_guest_by_id_not_found(guest_service):
    guest_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await guest_service.get_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Guest not found"

    guest_service.repo.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_guests(guest_service, guest_data):
    guest_service.repo.get_all.return_value = [guest_data]

    result = await guest_service.get_all()

    assert result == [guest_data]

    guest_service.repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_guest(guest_service, guest_data):
    updated_guest = {
        **guest_data,
        "first_name": "Updated",
    }

    guest_service.repo.update.return_value = updated_guest

    guest = GuestUpdate(
        id=updated_guest["id"],
        first_name="Updated",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )

    result = await guest_service.update(guest)

    assert result == updated_guest

    guest_service.repo.update.assert_awaited_once_with(
        id=updated_guest["id"],
        first_name="Updated",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )


@pytest.mark.asyncio
async def test_update_guest_not_found(guest_service):
    guest_service.repo.update.return_value = None

    guest = GuestUpdate(
        id=999,
        first_name="Name",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )

    with pytest.raises(HTTPException) as exc:
        await guest_service.update(guest)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Guest not found"

    guest_service.repo.update.assert_awaited_once_with(
        id=999,
        first_name="Name",
        last_name=None,
        email=None,
        phone=None,
        role=None,
        password_hash=None,
    )


@pytest.mark.asyncio
async def test_delete_guest(guest_service, guest_data):
    guest_service.repo.delete.return_value = guest_data

    guest = GuestDelete(id=guest_data["id"])

    result = await guest_service.delete(guest)

    assert result == guest_data

    guest_service.repo.delete.assert_awaited_once_with(id=guest_data["id"])


@pytest.mark.asyncio
async def test_delete_guest_not_found(guest_service):
    guest_service.repo.delete.return_value = None

    guest = GuestDelete(id=999)

    with pytest.raises(HTTPException) as exc:
        await guest_service.delete(guest)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Guest not found"

    guest_service.repo.delete.assert_awaited_once_with(id=999)
