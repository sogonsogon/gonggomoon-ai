from pydantic import BaseModel

class ExtractedExperienceMessage(BaseModel):
    id: int
    user_id: int
    file_asset_id: int
    job_type: str = "EXPERIENCE_EXTRACTION" # 작업 유형을 나타내는 필드 추가
    callback_url: str | None = None

class PortfolioStrategyGenerationMessage(BaseModel):
    user_id: int
    portfolio_strategy_id: int
    experiences: list[dict]
    position_type: str
    job_type: str = "PORTFOLIO_STRATEGY_GENERATION"
    industry_type: str
    callback_url: str | None = None
