from fastapi import HTTPException, status
from app.core.config import get_settings

INTERNAL_API_KEY = get_settings().internal_api_key

# 내부 API 키 검증 함수 - AI 서버의 민감한 엔드포인트 보호용
def verify_internal_api_key(x_internal_api_key: str | None) -> None:
    if x_internal_api_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal API key.",
        )
