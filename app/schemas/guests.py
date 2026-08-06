from datetime import datetime
from pydantic import BaseModel, EmailStr


class GuestResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime


class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class GuestUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class GuestDelete(BaseModel):
    id: int
