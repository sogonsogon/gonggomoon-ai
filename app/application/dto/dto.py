from pydantic import BaseModel

class ExtractedExperienceMessage(BaseModel):
    id: int
    user_id: int
    file_asset_id: int
    job_type: str = "EXPERIENCE_EXTRACTION" # 작업 유형을 나타내는 필드 추가
    callback_url: str | None = "http://host.docker.internal:8080/api/v1/callbacks/experience_extraction" # TODO : 실제 콜백 URL로 변경하기

