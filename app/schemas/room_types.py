from pydantic import BaseModel


class RoomTypeResponse(BaseModel):
    id: int
    room_type: str


class RoomTypeCreate(BaseModel):
    room_type: str


class RoomTypeUpdate(BaseModel):
    id: int
    room_type: str | None = None


class RoomTypeDelete(BaseModel):
    id: int
