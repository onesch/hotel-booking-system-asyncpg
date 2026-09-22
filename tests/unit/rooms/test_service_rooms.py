import pytest
from fastapi import HTTPException

from app.exceptions.database import RelatedEntityNotFoundError
from app.schemas.rooms import (
    RoomCreate,
    RoomDelete,
    RoomUpdate,
)


"""
Service -> correctly calls the Repository
        -> correctly handles the Repository result
"""


@pytest.mark.asyncio
async def test_create_room(room_service, room_data):
    room_service.repo.create.return_value = room_data
    room = RoomCreate(
        room_number=room_data["room_number"],
        room_floor=room_data["room_floor"],
        is_active=room_data["is_active"],
        hotel_id=room_data["hotel_id"],
        room_type_id=room_data["room_type_id"],
    )

    result = await room_service.create(room=room)

    assert result == room_data
    room_service.repo.create.assert_awaited_once_with(
        room_number=room_data["room_number"],
        room_floor=room_data["room_floor"],
        is_active=room_data["is_active"],
        hotel_id=room_data["hotel_id"],
        room_type_id=room_data["room_type_id"],
    )


@pytest.mark.asyncio
async def test_create_room_with_missing_related_entity(room_service, room_data):
    room_service.repo.create.side_effect = RelatedEntityNotFoundError
    room = RoomCreate(
        room_number=room_data["room_number"],
        room_floor=room_data["room_floor"],
        is_active=room_data["is_active"],
        hotel_id=room_data["hotel_id"],
        room_type_id=room_data["room_type_id"],
    )

    with pytest.raises(HTTPException) as exc:
        await room_service.create(room=room)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel or room type not found"
    room_service.repo.create.assert_awaited_once_with(
        room_number=room_data["room_number"],
        room_floor=room_data["room_floor"],
        is_active=room_data["is_active"],
        hotel_id=room_data["hotel_id"],
        room_type_id=room_data["room_type_id"],
    )


@pytest.mark.asyncio
async def test_get_room_by_id(room_service, room_data):
    room_service.repo.get_by_id.return_value = room_data

    result = await room_service.get_by_id(room_data["id"])

    assert result == room_data
    room_service.repo.get_by_id.assert_awaited_once_with(room_data["id"])


@pytest.mark.asyncio
async def test_get_room_by_id_not_found(room_service):
    room_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await room_service.get_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room not found"
    room_service.repo.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_rooms(room_service, room_data):
    room_service.repo.get_all.return_value = [room_data]

    result = await room_service.get_all()

    assert result == [room_data]
    room_service.repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_room(room_service, room_data):
    updated_room = {
        **room_data,
        "room_number": "202",
        "is_active": False,
    }
    room_service.repo.update.return_value = updated_room
    room = RoomUpdate(
        id=updated_room["id"],
        room_number="202",
        room_floor=None,
        is_active=False,
        hotel_id=None,
        room_type_id=None,
    )

    result = await room_service.update(room)

    assert result == updated_room
    room_service.repo.update.assert_awaited_once_with(
        id=updated_room["id"],
        room_number="202",
        room_floor=None,
        is_active=False,
        hotel_id=None,
        room_type_id=None,
    )


@pytest.mark.asyncio
async def test_update_room_not_found(room_service):
    room_service.repo.update.return_value = None
    room = RoomUpdate(
        id=999,
        room_number="999",
        room_floor=None,
        is_active=None,
        hotel_id=None,
        room_type_id=None,
    )

    with pytest.raises(HTTPException) as exc:
        await room_service.update(room)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room not found"
    room_service.repo.update.assert_awaited_once_with(
        id=999,
        room_number="999",
        room_floor=None,
        is_active=None,
        hotel_id=None,
        room_type_id=None,
    )


@pytest.mark.asyncio
async def test_update_room_with_missing_related_entity(room_service, room_data):
    room_service.repo.update.side_effect = RelatedEntityNotFoundError
    room = RoomUpdate(
        id=room_data["id"],
        room_number=None,
        room_floor=None,
        is_active=None,
        hotel_id=999,
        room_type_id=None,
    )

    with pytest.raises(HTTPException) as exc:
        await room_service.update(room)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Hotel or room type not found"
    room_service.repo.update.assert_awaited_once_with(
        id=room_data["id"],
        room_number=None,
        room_floor=None,
        is_active=None,
        hotel_id=999,
        room_type_id=None,
    )


@pytest.mark.asyncio
async def test_delete_room(room_service, room_data):
    room_service.repo.delete.return_value = room_data
    room = RoomDelete(id=room_data["id"])

    result = await room_service.delete(room)

    assert result == room_data
    room_service.repo.delete.assert_awaited_once_with(id=room_data["id"])


@pytest.mark.asyncio
async def test_delete_room_not_found(room_service):
    room_service.repo.delete.return_value = None
    room = RoomDelete(id=999)

    with pytest.raises(HTTPException) as exc:
        await room_service.delete(room)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room not found"
    room_service.repo.delete.assert_awaited_once_with(id=999)
