from pydantic import BaseModel
from datetime import datetime


class RoomTypeCountResponse(BaseModel):
    room_type_id: int
    room_type: str
    room_count: int


class MonthlyBookingsResponse(BaseModel):
    month: datetime
    booking_count: int


class RoomTypePopularityResponse(BaseModel):
    room_type_id: int
    room_type: str
    booking_count: int
