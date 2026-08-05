from fastapi import FastAPI

from app.routers.guests import router as guests_api_router


def create_app() -> FastAPI:
    """
    Function for create FastAPI app instance.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    app = FastAPI()

    # routers
    app.include_router(guests_api_router, prefix="/guests")

    return app

app = create_app()
