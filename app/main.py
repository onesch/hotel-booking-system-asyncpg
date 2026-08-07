from fastapi import FastAPI

from app.routers.guests import router as guests_api_router
from app.routers.hotels import router as hotels_api_router


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

    return app

app = create_app()
