from pydantic import BaseModel
from app.application.container import settings

CALLBACK_URL = settings.call_back_url
class ExtractedExperienceMessage(BaseModel):
    id: int
    user_id: int
    file_asset_id: int
    job_type: str = "EXPERIENCE_EXTRACTION" # 작업 유형을 나타내는 필드 추가
    callback_url: str | None = CALLBACK_URL + "experience_extraction"
