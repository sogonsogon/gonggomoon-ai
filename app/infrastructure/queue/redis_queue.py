from redis import Redis

from app.application.ports.ports import JobQueuePort
from app.application.dto.dto import ExtractedExperienceMessage


# TODO : ExtractedExperienceMessage를 좀 더 범용적으로 사용할 수 있도록 리팩토링.
class RedisJobQueue(JobQueuePort):
    def __init__(self, redis_url: str, queue_key: str = "ai:jobs") -> None:
        self.client = Redis.from_url(redis_url, decode_responses=True)
        self.queue_key = queue_key

    def enqueue(self, message: ExtractedExperienceMessage) -> None:
        self.client.rpush(self.queue_key, message.model_dump_json())

    def dequeue(self) -> ExtractedExperienceMessage | None:
        payload = self.client.lpop(self.queue_key)
        if payload is None:
            return None
        return ExtractedExperienceMessage.model_validate_json(payload)

    def size(self) -> int:
        return int(self.client.llen(self.queue_key))
