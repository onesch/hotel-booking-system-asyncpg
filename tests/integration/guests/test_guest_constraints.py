import pytest

from app.exceptions.database import GuestAlreadyExistsError


# --------- UNIQUE -----------


@pytest.mark.asyncio
async def test_create_guest_with_duplicate_email(
    repository,
    clean_database,
):
    await repository.create(
        first_name="Test1",
        last_name="User1",
        email="test1@example.com",
        phone="+111111111",
        password_hash="test_hash1",
    )

    with pytest.raises(GuestAlreadyExistsError):
        await repository.create(
            first_name="Test2",
            last_name="User2",
            email="test1@example.com",
            phone="+222222222",
            password_hash="test_hash2",
        )


@pytest.mark.asyncio
async def test_create_guest_with_duplicate_phone(
    repository,
    clean_database,
):
    await repository.create(
        first_name="Test1",
        last_name="User1",
        email="test1@example.com",
        phone="+111111111",
        password_hash="test_hash1",
    )

    with pytest.raises(GuestAlreadyExistsError):
        await repository.create(
            first_name="Test2",
            last_name="User2",
            email="test2@example.com",
            phone="+111111111",
            password_hash="test_hash2",
        )
