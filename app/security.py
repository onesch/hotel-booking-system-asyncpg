import re
from fastapi.security import HTTPBasic
from passlib.context import CryptContext
from pydantic import SecretStr, field_validator


# HTTP Basic authentication
security = HTTPBasic()

# Password hashing using bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def hash_password(password: SecretStr) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password.get_secret_value())


class PasswordValidationMixin:
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:
        password = value.get_secret_value()

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_]", password):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value
