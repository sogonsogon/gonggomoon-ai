from pydantic import BaseModel
from app.core.enums import JobType

class BaseJobMessage(BaseModel):
    id: int | None = None
    user_id: int
    job_type: JobType
    callback_url: str | None = None


class ExtractedExperienceMessage(BaseJobMessage):
    file_asset_id: int
    job_type: JobType = JobType.EXPERIENCE_EXTRACTION

class PortfolioStrategyGenerationMessage(BaseJobMessage):
    experiences: list[dict]
    position_type: str
    industry_type: str
    job_type: JobType = JobType.PORTFOLIO_STRATEGY_GENERATION
