from fastapi import FastAPI

from app.api.routers.health import health_router
from app.api.routers.job_router import jobs_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name, version=settings.service_version)
    app.include_router(health_router)
    app.include_router(jobs_router)
    return app


app = create_app()
