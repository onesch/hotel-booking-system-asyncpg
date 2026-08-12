from fastapi import FastAPI

from app.routers.guests import router as guests_api_router
from app.routers.hotels import router as hotels_api_router
from app.routers.rooms import router as rooms_api_router
from app.routers.room_types import router as room_types_api_router


def create_app() -> FastAPI:
    """
    Function for create FastAPI app instance.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    app = FastAPI()

    # routers
    app.include_router(guests_api_router, prefix="/guests")
    app.include_router(hotels_api_router, prefix="/hotels")
    app.include_router(rooms_api_router, prefix="/rooms")
    app.include_router(room_types_api_router, prefix="/room_types")

    return app

app = create_app()
