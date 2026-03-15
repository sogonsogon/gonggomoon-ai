from pydantic import BaseModel, Field

class InterviewStrategyGenerationRequest(BaseModel):
    user_id : int = Field(description="면접 전략을 생성할 사용자 ID")
    file_asset_id : int = Field(description="면접 전략 생성을 위한 파일 자산 ID")