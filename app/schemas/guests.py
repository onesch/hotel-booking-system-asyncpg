from datetime import datetime
from pydantic import BaseModel, EmailStr


class GuestResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str
    created_at: datetime


class GuestRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class GuestUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    role: str | None = None


class GuestDelete(BaseModel):
    id: int
