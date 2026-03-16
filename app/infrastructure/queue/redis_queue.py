from redis import Redis

from app.application.ports.ports import JobQueuePort
import json

from app.application.dto.dto import (
    BaseJobMessage,
    ExtractedExperienceMessage,
    PortfolioStrategyGenerationMessage,
    InterviewStrategyGenerationMessage
)
from app.core.enums import JobType


# TODO : ExtractedExperienceMessage를 좀 더 범용적으로 사용할 수 있도록 리팩토링.
class RedisJobQueue(JobQueuePort):
    def __init__(self, redis_url: str, queue_key: str = "ai:jobs") -> None:
        self.client = Redis.from_url(redis_url, decode_responses=True)
        self.queue_key = queue_key

    def enqueue(self, message) -> None:
        self.client.rpush(self.queue_key, message.model_dump_json())

    def dequeue(self):
        payload = self.client.lpop(self.queue_key)
        if payload is None:
            return None

        data = json.loads(payload)

        job_type = data.get("job_type")

        if job_type == JobType.EXPERIENCE_EXTRACTION.value:
            return ExtractedExperienceMessage.model_validate(data)

        if job_type == JobType.PORTFOLIO_STRATEGY_GENERATION.value:
            return PortfolioStrategyGenerationMessage.model_validate(data)
        
        if job_type == JobType.INTERVIEW_STRATEGY_GENERATION.value:
            return InterviewStrategyGenerationMessage.model_validate(data)
        
        if job_type == JobType.POST_ANALYSIS.value:
            return BaseJobMessage.model_validate(data)

        raise ValueError(f"Unsupported job_type in queue: {job_type}")
    def size(self) -> int:
        return int(self.client.llen(self.queue_key))
