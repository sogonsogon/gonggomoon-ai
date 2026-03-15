from pydantic import BaseModel, Field

class InterviewStrategyGenerationRequest(BaseModel):
    user_id : int = Field(description="면접 전략을 생성할 사용자 ID")
    interview_strategy_id : int = Field(description="면접 전략 ID")