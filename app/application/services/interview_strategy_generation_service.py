from app.api.dto.interview_strategy_generation import InterviewStrategyGenerationRequest
from app.application.dto.dto import InterviewStrategyGenerationMessage
from app.application.ports.ports import JobQueuePort

class InterviewStrategyGenerationService:
    def __init__(self, queue: JobQueuePort, callback_url: str):
        self.queue = queue
        self.callback_url = callback_url

    def enqueue_interview_strategy_generation(self, request: InterviewStrategyGenerationRequest) -> None:
        # JobMessage 생성
        message = InterviewStrategyGenerationMessage(
            user_id=request.user_id,
            file_asset_id=request.file_asset_id,
            callback_url=self.callback_url
        )

        # 큐에 메시지 넣기
        self.queue.enqueue(message)