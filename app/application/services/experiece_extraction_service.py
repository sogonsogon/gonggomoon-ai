from app.application.ports.ports import JobQueuePort, ExtractedExperienceRepositoryPort
from app.api.dto.experience_extraction import ExperienceExtractionRequest
from app.application.dto.dto import ExtractedExperienceMessage

class ExperienceExtractionService:
    def __init__(self, queue: JobQueuePort, repository: ExtractedExperienceRepositoryPort, callback_url: str | None) -> None:
        self.queue = queue
        self.repository = repository
        self.callback_url = callback_url

    def enqueue_experience_extraction(self, request: ExperienceExtractionRequest) -> None:
        # Repository에서 ExtractedExperience 조회
        extracted_experiences = self.repository.get_extracted_experiences(request.extracted_experience_ids)

        # 거기서 file_asset_id, user_id 등 필요한 정보도 같이 조회해서 JobMessage 생성에 활용
        file_asset_ids = []
        for extracted_experience in extracted_experiences:
            extrction_set = {"extracted_experience_id": extracted_experience.id, "file_asset_id": extracted_experience.file_asset_id}
            file_asset_ids.append(extrction_set)

        # JobMessage 생성
        message = ExtractedExperienceMessage(
            id=extracted_experience.id,
            user_id=extracted_experience.user_id,
            file_asset_ids=file_asset_ids,
            callback_url=self.callback_url
        )

        # 큐에 메시지 넣기
        self.queue.enqueue(message)