from app.api.dto.interview_strategy_generation import InterviewStrategyGenerationRequest
from app.application.dto.dto import InterviewStrategyGenerationMessage
from app.application.ports.ports import JobQueuePort
from app.core.enums import JobType

class InterviewStrategyGenerationService:
    def __init__(self, queue: JobQueuePort, callback_url: str):
        self.queue = queue
        self.callback_url = callback_url

    def enqueue_interview_strategy_generation(self, request: InterviewStrategyGenerationRequest) -> None:
        # JobMessage 생성
        message = InterviewStrategyGenerationMessage(
            id=request.interview_strategy_id,
            user_id=request.user_id,
            job_type=JobType.INTERVIEW_STRATEGY_GENERATION,
            callback_url=self.callback_url
        )

        # 큐에 메시지 넣기
        self.queue.enqueue(message)