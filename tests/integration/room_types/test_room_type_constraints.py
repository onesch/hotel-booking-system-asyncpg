import pytest

from app.exceptions.database import (
    RoomTypeAlreadyExistsError,
    RoomTypeInUseError,
)


# --------- UNIQUE -----------

@pytest.mark.asyncio
async def test_create_room_type_duplicate(
    repository,
    clean_database,
):
    await repository.create(room_type="Standard")

    with pytest.raises(RoomTypeAlreadyExistsError):
        await repository.create(room_type="Standard")


# --------- RESTRICT -----------


@pytest.mark.asyncio
async def test_delete_room_type_restricted_when_used(
    repository,
    test_db,
    clean_database,
    hotel,
):
    room_type = await repository.create(room_type="Standard")

    await test_db.fetchrow(
        """
        INSERT INTO rooms (
            room_number,
            room_floor,
            is_active,
            hotel_id,
            room_type_id
        )
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id;
        """,
        "101",
        "1",
        True,
        hotel["id"],
        room_type["id"],
    )

    with pytest.raises(RoomTypeInUseError):
        await repository.delete(id=room_type["id"])
