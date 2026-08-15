from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from app.security import security
from app.services.auth import AuthService


auth_service = AuthService()


async def get_current_guest(
    credentials: HTTPBasicCredentials = Depends(security),
) -> dict:
    """
    Return the authenticated guest.
    """
    guest = await auth_service.authenticate(
        credentials.username,
        credentials.password,
    )

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return guest


async def require_admin(
    current_guest=Depends(get_current_guest),
) -> dict:
    """
    Require the authenticated guest to be an admin.
    """
    if current_guest["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_guest


async def require_business(
    current_guest=Depends(get_current_guest),
) -> dict:
    """
    Require the authenticated guest to be a business account.
    """
    if current_guest["role"] != "business":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business access required",
        )

    return current_guest


def require_owner_or_admin(
    current_guest: dict,
    owner_id: int,
) -> None:
    if (
        current_guest["role"] != "admin"
        and current_guest["id"] != owner_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own resources",
        )
