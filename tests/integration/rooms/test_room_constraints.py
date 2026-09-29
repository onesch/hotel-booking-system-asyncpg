import asyncpg
import pytest

from app.exceptions.database import RelatedEntityNotFoundError


# -------- FOREIGN KEY --------


@pytest.mark.asyncio
async def test_create_room_with_nonexistent_hotel(
    integration_room_repository,
    clean_database,
    room_type,
):
    with pytest.raises(RelatedEntityNotFoundError):
        await integration_room_repository.create(
            room_number="101",
            room_floor="1",
            is_active=True,
            hotel_id=999999,
            room_type_id=room_type["id"],
        )


@pytest.mark.asyncio
async def test_create_room_with_nonexistent_room_type(
    integration_room_repository,
    clean_database,
    hotel,
):
    with pytest.raises(RelatedEntityNotFoundError):
        await integration_room_repository.create(
            room_number="101",
            room_floor="1",
            is_active=True,
            hotel_id=hotel["id"],
            room_type_id=999999,
        )


# ---------- CASCADE ----------


@pytest.mark.asyncio
async def test_delete_hotel_cascades_to_rooms(
    test_db,
    integration_room_repository,
    clean_database,
    hotel,
    room_type,
):
    room = await integration_room_repository.create(
        room_number="101",
        room_floor="1",
        is_active=True,
        hotel_id=hotel["id"],
        room_type_id=room_type["id"],
    )

    await test_db.execute(
        """
        DELETE FROM hotels
        WHERE id = $1;
        """,
        hotel["id"],
    )

    result = await integration_room_repository.get_by_id(room["id"])

    assert result is None


# ---------- RESTRICT ----------


@pytest.mark.asyncio
async def test_delete_room_type_used_by_room_is_restricted(
    test_db,
    integration_room_repository,
    clean_database,
    hotel,
    room_type,
):
    room = await integration_room_repository.create(
        room_number="101",
        room_floor="1",
        is_active=True,
        hotel_id=hotel["id"],
        room_type_id=room_type["id"],
    )

    with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
        await test_db.execute(
            """
            DELETE FROM room_types
            WHERE id = $1;
            """,
            room_type["id"],
        )

    result = await integration_room_repository.get_by_id(room["id"])

    assert result is not None
    assert result["id"] == room["id"]


# ---------- NOT NULL ----------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field",
    [
        "room_number",
        "room_floor",
        "hotel_id",
        "room_type_id",
    ],
)
async def test_create_room_with_null_required_field(
    field,
    integration_room_repository,
    clean_database,
    hotel,
    room_type,
):
    room_data = {
        "room_number": "101",
        "room_floor": "1",
        "is_active": True,
        "hotel_id": hotel["id"],
        "room_type_id": room_type["id"],
    }
    room_data[field] = None

    with pytest.raises(asyncpg.exceptions.NotNullViolationError):
        await integration_room_repository.create(**room_data)
