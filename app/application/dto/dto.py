from pydantic import BaseModel

from app.core.enums import JobType


class BaseJobMessage(BaseModel):
    id: int | None = None
    user_id: int
    job_type: JobType
    callback_url: str | None = None
    attempt_count: int = 1
    max_attempts: int = 3


class ExtractedExperienceMessage(BaseJobMessage):
    file_asset_ids: list[dict[str, int]]
    job_type: JobType = JobType.EXPERIENCE_EXTRACTION


class PortfolioStrategyGenerationMessage(BaseJobMessage):
    experiences: list[dict]
    position_type: str
    industry_type: str
    job_type: JobType = JobType.PORTFOLIO_STRATEGY_GENERATION


class InterviewStrategyGenerationMessage(BaseJobMessage):
    job_type: JobType = JobType.INTERVIEW_STRATEGY_GENERATION
