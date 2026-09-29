from pydantic import BaseModel, EmailStr, SecretStr

from app.schemas.guests import BusinessResponse, GuestResponse
from app.security import PasswordValidationMixin


class GuestRegister(BaseModel, PasswordValidationMixin):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: SecretStr


class GuestRegisterResponse(GuestResponse):
    message: str


class BusinessRegister(BaseModel, PasswordValidationMixin):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: SecretStr


class BusinessRegisterResponse(BusinessResponse):
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr
