import pytest
from fastapi import HTTPException

from app.exceptions.database import (
    RoomTypeAlreadyExistsError,
    RoomTypeInUseError,
)
from app.schemas.room_types import (
    RoomTypeCreate,
    RoomTypeUpdate,
    RoomTypeDelete,
)

"""
Service -> correctly calls the Repository
        -> correctly handles the Repository result
"""

@pytest.mark.asyncio
async def test_create_room_type(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.create.return_value = room_type_data

    room_type = RoomTypeCreate(
        room_type=room_type_data["room_type"],
    )

    result = await room_type_service.create(
        room_type=room_type,
    )

    assert result == room_type_data

    room_type_service.repo.create.assert_awaited_once_with(
        room_type=room_type_data["room_type"],
    )


@pytest.mark.asyncio
async def test_create_room_type_already_exists(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.create.side_effect = (
        RoomTypeAlreadyExistsError()
    )

    room_type = RoomTypeCreate(
        room_type=room_type_data["room_type"],
    )

    with pytest.raises(HTTPException) as exc:
        await room_type_service.create(
            room_type=room_type,
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Room type already exists"

    room_type_service.repo.create.assert_awaited_once_with(
        room_type=room_type_data["room_type"],
    )


@pytest.mark.asyncio
async def test_get_room_type_by_id(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.get_by_id.return_value = (
        room_type_data
    )

    result = await room_type_service.get_by_id(
        room_type_data["id"]
    )

    assert result == room_type_data

    room_type_service.repo.get_by_id.assert_awaited_once_with(
        room_type_data["id"]
    )


@pytest.mark.asyncio
async def test_get_room_type_by_id_not_found(
    room_type_service,
):
    room_type_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await room_type_service.get_by_id(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room type not found"

    room_type_service.repo.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_room_types(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.get_all.return_value = [
        room_type_data
    ]

    result = await room_type_service.get_all()

    assert result == [room_type_data]

    room_type_service.repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_room_type(
    room_type_service,
    room_type_data,
):
    updated_room_type = {
        **room_type_data,
        "room_type": "Updated",
    }

    room_type_service.repo.update.return_value = (
        updated_room_type
    )

    room_type = RoomTypeUpdate(
        id=room_type_data["id"],
        room_type="Updated",
    )

    result = await room_type_service.update(room_type)

    assert result == updated_room_type

    room_type_service.repo.update.assert_awaited_once_with(
        id=room_type_data["id"],
        room_type="Updated",
    )


@pytest.mark.asyncio
async def test_update_room_type_already_exists(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.update.side_effect = (
        RoomTypeAlreadyExistsError()
    )

    room_type = RoomTypeUpdate(
        id=room_type_data["id"],
        room_type="Updated",
    )

    with pytest.raises(HTTPException) as exc:
        await room_type_service.update(room_type)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Room type already exists"

    room_type_service.repo.update.assert_awaited_once_with(
        id=room_type_data["id"],
        room_type="Updated",
    )


@pytest.mark.asyncio
async def test_update_room_type_not_found(
    room_type_service,
):
    room_type_service.repo.update.return_value = None

    room_type = RoomTypeUpdate(
        id=999,
        room_type="Updated",
    )

    with pytest.raises(HTTPException) as exc:
        await room_type_service.update(room_type)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room type not found"

    room_type_service.repo.update.assert_awaited_once_with(
        id=999,
        room_type="Updated",
    )


@pytest.mark.asyncio
async def test_delete_room_type(
    room_type_service,
    room_type_data,
):
    room_type_service.repo.delete.return_value = (
        room_type_data
    )

    room_type = RoomTypeDelete(
        id=room_type_data["id"],
    )

    result = await room_type_service.delete(room_type)

    assert result == room_type_data

    room_type_service.repo.delete.assert_awaited_once_with(
        id=room_type_data["id"]
    )


@pytest.mark.asyncio
async def test_delete_room_type_not_found(
    room_type_service,
):
    room_type_service.repo.delete.return_value = None

    room_type = RoomTypeDelete(id=999)

    with pytest.raises(HTTPException) as exc:
        await room_type_service.delete(room_type)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Room type not found"

    room_type_service.repo.delete.assert_awaited_once_with(
        id=999
    )


@pytest.mark.asyncio
async def test_delete_room_type_in_use(
    room_type_service,
):
    room_type_service.repo.delete.side_effect = (
        RoomTypeInUseError()
    )

    room_type = RoomTypeDelete(id=1)

    with pytest.raises(HTTPException) as exc:
        await room_type_service.delete(room_type)

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Room type is used by one or more rooms"
    )

    room_type_service.repo.delete.assert_awaited_once_with(
        id=1
    )
