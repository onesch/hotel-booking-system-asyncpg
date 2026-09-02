from datetime import date
from pydantic import BaseModel, model_validator


class DateValidationMixin:
    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out_date <= self.check_in_date:
            raise ValueError(
                "Check-out date must be after check-in date"
            )
        return self


class BookingCreate(BaseModel, DateValidationMixin):
    room_id: int
    check_in_date: date
    check_out_date: date


class BookingResponse(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date


class BookingUpdate(BaseModel, DateValidationMixin):
    id: int
    check_in_date: date
    check_out_date: date


class BookingDelete(BaseModel):
    id: int
