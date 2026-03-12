from datetime import datetime, timezone
from typing import Any

from app.application.dto.dto import ExtractedExperienceMessage
from app.core.enums import JobType
from app.domain.experience_extraction.processor import ExperienceExtractionProcessor


class JobHandler:
    # TODO : processor가 늘어날 때 마다 추가해주자
    def __init__(self, experience_processor: ExperienceExtractionProcessor) -> None:
        self.experience_processor = experience_processor

    # TODO : 여기서 job_type에 따라서 다른 처리를 할 수 있도록 해야 함.
    def handle(self, message: ExtractedExperienceMessage) -> dict[str, Any]:
        if message.job_type == JobType.EXPERIENCE_EXTRACTION:
            result = self.experience_processor.process(message.file_asset_id)
        else:
            raise ValueError(f"Unsupported job type: {message.job_type}")

        return {
            "type" : message.job_type, # String임 !
            "id" : message.id, # 각 테스크 마다 받아온 아이디 값
            "user_id": str(message.user_id),
            "status": "COMPLETED",
            "result": result,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
