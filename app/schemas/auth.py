import re
from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class GuestRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> str:
        value = value.get_secret_value()

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
            
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
            
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
            
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_]", value):
            raise ValueError("Password must contain at least one special character.")

        value = SecretStr(value)
        return value


class BusinessRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: SecretStr


class BusinessRegisterResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str
