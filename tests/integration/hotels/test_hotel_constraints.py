import pytest
import asyncpg


# -------- FOREIGN KEY --------


@pytest.mark.asyncio
async def test_create_hotel_with_nonexistent_owner(
    integration_hotel_repository,
    clean_database,
):
    with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
        await integration_hotel_repository.create(
            name="Test Hotel",
            address="Test Address",
            description="Test Description",
            owner_id=999999,
        )


# ---------- CASCADE ----------


@pytest.mark.asyncio
async def test_delete_guest_cascades_to_hotels(
    test_db,
    integration_hotel_repository,
    clean_database,
    guest,
):
    hotel = await integration_hotel_repository.create(
        name="Test Hotel",
        address="Test Address",
        description="Test Description",
        owner_id=guest["id"],
    )

    await test_db.execute(
        """
        DELETE FROM guests
        WHERE id = $1;
        """,
        guest["id"],
    )

    result = await integration_hotel_repository.get_by_id(hotel["id"])

    assert result is None
