from app.api.dto.post_analysis_request import PostAnalysisRequest
from app.application.dto.dto import BaseJobMessage
from app.application.ports.ports import JobQueuePort
from app.core.enums import JobType

class PostAnalysisService:
    def __init__(self, queue:JobQueuePort, callback_url:str):
        self.queue = queue
        self.callback_url = callback_url

    def enqueue_post_analysis(self, request:PostAnalysisRequest):
        # JobMessage 생성
        message = BaseJobMessage(
            id=request.post_id,
            user_id=request.user_id,
            job_type=JobType.POST_ANALYSIS,
            callback_url=self.callback_url
        )

        # 큐에 메시지 넣기
        self.queue.enqueue(message)