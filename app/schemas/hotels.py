from datetime import datetime
from pydantic import BaseModel


class HotelResponse(BaseModel):
    id: int
    name: str
    address: str
    description: str | None
    created_at: datetime


class HotelCreate(BaseModel):
    name: str
    address: str
    description: str | None = None


class HotelUpdate(BaseModel):
    id: int
    name: str | None = None
    address: str | None = None
    description: str | None = None


class HotelDelete(BaseModel):
    id: int
