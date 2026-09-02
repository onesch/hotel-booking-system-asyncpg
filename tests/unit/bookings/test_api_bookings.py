import pytest
from datetime import date

from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.main import app


"""
HTTP request -> Router -> mock BookingService
"""


@pytest.mark.asyncio
async def test_create_booking(
    api_booking_service,
    booking_data,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.create.return_value = booking_data

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "room_id": booking_data["room_id"],
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": booking_data["check_out_date"].isoformat(),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.post(
            "/bookings/create",
            json=payload,
        )

    assert response.status_code == 200

    expected_response = {
        **booking_data,
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": booking_data["check_out_date"].isoformat(),
    }

    assert response.json() == expected_response

    api_booking_service.create.assert_awaited_once()

    booking = api_booking_service.create.call_args.kwargs["booking"]
    guest_id = api_booking_service.create.call_args.kwargs["guest_id"]

    assert booking.room_id == booking_data["room_id"]
    assert booking.check_in_date == booking_data["check_in_date"]
    assert booking.check_out_date == booking_data["check_out_date"]
    assert guest_id == override_current_guest["id"]


@pytest.mark.asyncio
async def test_get_booking_by_id(
    api_booking_service,
    booking_data,
    monkeypatch,
):
    api_booking_service.get_by_id.return_value = booking_data

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get(
            f"/bookings/{booking_data['id']}"
        )

    assert response.status_code == 200

    expected_response = {
        **booking_data,
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": booking_data["check_out_date"].isoformat(),
    }

    assert response.json() == expected_response

    api_booking_service.get_by_id.assert_awaited_once_with(
        booking_data["id"]
    )


@pytest.mark.asyncio
async def test_get_booking_by_id_not_found(
    api_booking_service,
    monkeypatch,
):
    api_booking_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Booking not found",
    )

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/bookings/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}

    api_booking_service.get_by_id.assert_awaited_once_with(999)


@pytest.mark.asyncio
async def test_get_all_bookings(
    api_booking_service,
    booking_data,
    monkeypatch,
):
    api_booking_service.get_all.return_value = [booking_data]

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/bookings/")

    assert response.status_code == 200

    expected_response = [{
        **booking_data,
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": booking_data["check_out_date"].isoformat(),
    }]

    assert response.json() == expected_response

    api_booking_service.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_booking(
    api_booking_service,
    booking_data,
    override_current_guest,
    monkeypatch,
):
    updated_booking = {
        **booking_data,
        "check_out_date": date(2026, 10, 20),
    }

    api_booking_service.get_by_id.return_value = booking_data
    api_booking_service.update.return_value = updated_booking

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "id": booking_data["id"],
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": date(2026, 10, 20).isoformat(),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/bookings/update",
            json=payload,
        )

    assert response.status_code == 200

    expected_response = {
        **booking_data,
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": date(2026, 10, 20).isoformat(),
    }

    assert response.json() == expected_response

    api_booking_service.get_by_id.assert_awaited_once_with(
        booking_data["id"]
    )
    api_booking_service.update.assert_awaited_once()

    booking = api_booking_service.update.call_args.kwargs["booking"]
    guest_id = api_booking_service.update.call_args.kwargs["guest_id"]

    assert booking.id == booking_data["id"]
    assert booking.check_in_date == booking_data["check_in_date"]
    assert booking.check_out_date == date(2026, 10, 20)
    assert guest_id == override_current_guest["id"]


@pytest.mark.asyncio
async def test_update_booking_not_found(
    api_booking_service,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Booking not found",
    )

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "id": 999,
        "room_id": 1,
        "check_in_date": date(2026, 10, 10).isoformat(),
        "check_out_date": date(2026, 10, 15).isoformat(),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/bookings/update",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}

    api_booking_service.get_by_id.assert_awaited_once_with(999)
    api_booking_service.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_booking_forbidden(
    api_booking_service,
    booking_data,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.get_by_id.return_value = {
        **booking_data,
        "guest_id": 999,
    }

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "id": booking_data["id"],
        "room_id": booking_data["room_id"],
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": date(2026, 10, 20).isoformat(),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.patch(
            "/bookings/update",
            json=payload,
        )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You can only manage your own resources"
    }

    api_booking_service.get_by_id.assert_awaited_once_with(
        booking_data["id"]
    )
    api_booking_service.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_booking(
    api_booking_service,
    booking_data,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.get_by_id.return_value = booking_data
    api_booking_service.delete.return_value = booking_data

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "id": booking_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.request(
            "DELETE",
            "/bookings/delete",
            json=payload,
        )

    assert response.status_code == 200

    expected_response = {
        **booking_data,
        "check_in_date": booking_data["check_in_date"].isoformat(),
        "check_out_date": booking_data["check_out_date"].isoformat(),
    }

    assert response.json() == expected_response

    api_booking_service.get_by_id.assert_awaited_once_with(
        booking_data["id"]
    )
    api_booking_service.delete.assert_awaited_once()

    kwargs = api_booking_service.delete.call_args.kwargs

    assert kwargs["booking_id"] == booking_data["id"]
    assert kwargs["guest_id"] == override_current_guest["id"]


@pytest.mark.asyncio
async def test_delete_booking_not_found(
    api_booking_service,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.get_by_id.side_effect = HTTPException(
        status_code=404,
        detail="Booking not found",
    )

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
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
            "/bookings/delete",
            json=payload,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}

    api_booking_service.get_by_id.assert_awaited_once_with(999)
    api_booking_service.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_booking_forbidden(
    api_booking_service,
    booking_data,
    override_current_guest,
    monkeypatch,
):
    api_booking_service.get_by_id.return_value = {
        **booking_data,
        "guest_id": 999,
    }

    monkeypatch.setattr(
        "app.routers.bookings.bookings_service",
        api_booking_service,
    )

    payload = {
        "id": booking_data["id"],
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.request(
            "DELETE",
            "/bookings/delete",
            json=payload,
        )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You can only manage your own resources"
    }

    api_booking_service.get_by_id.assert_awaited_once_with(
        booking_data["id"]
    )
    api_booking_service.delete.assert_not_awaited()
