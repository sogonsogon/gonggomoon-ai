# 헬스 체크 API
from datetime import datetime, timezone
from fastapi import APIRouter

from app.api.dto.health import HealthResponse


health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai-server",
        now=datetime.now(timezone.utc),
    )
