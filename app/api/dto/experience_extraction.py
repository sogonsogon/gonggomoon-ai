from pydantic import BaseModel, Field

class ExperienceExtractionRequest(BaseModel):
    extracted_experience_ids: list[int] = Field(description="API 서버가 생성한 추출 작업 IDs")