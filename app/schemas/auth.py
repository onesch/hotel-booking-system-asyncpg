from pydantic import BaseModel, EmailStr

from app.schemas.guests import GuestResponse
from app.schemas.hotels import HotelResponse


class GuestRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class BusinessRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str

    hotel_name: str
    hotel_address: str
    hotel_description: str | None = None


class BusinessRegisterResponse(BaseModel):
    guest: GuestResponse
    hotel: HotelResponse
