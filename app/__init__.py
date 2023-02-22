"""Top-level package, contains primary app setup and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .routers import routers


def create_app() -> FastAPI:
    app = FastAPI(title="acme-service-merchant-settle", version="0.0.1")

    register_events(app)
    register_middlewares(app)
    register_routers(app)

    return app


def register_events(app: FastAPI):
    """Register lifecycle events on the app."""

    @app.on_event("startup")
    async def startup():
        logger.debug("Starting service")

    @app.on_event("shutdown")
    async def shutdown():
        logger.debug("Stopping service")


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)


app = create_app()
