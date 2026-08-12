from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: int
    room_number: str
    room_floor: str
    is_active: bool
    hotel_id: int
    room_type_id: int


class RoomCreate(BaseModel):
    room_number: str
    room_floor: str
    is_active: bool = False
    hotel_id: int
    room_type_id: int


class RoomUpdate(BaseModel):
    id: int
    room_number: str | None = None
    room_floor: str | None = None
    is_active: bool | None = None
    hotel_id: int | None = None
    room_type_id: int | None = None


class RoomDelete(BaseModel):
    id: int
