from pydantic import BaseModel, EmailStr


class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class GuestResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
