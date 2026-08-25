from datetime import date
from pydantic import BaseModel, model_validator


class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out_date <= self.check_in_date:
            raise ValueError(
                "Check-out date must be after check-in date"
            )
        return self


class BookingResponse(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date


class BookingUpdate(BaseModel):
    id: int
    check_in_date: date
    check_out_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out_date <= self.check_in_date:
            raise ValueError(
                "Check-out date must be after check-in date"
            )
        return self


class BookingDelete(BaseModel):
    id: int
