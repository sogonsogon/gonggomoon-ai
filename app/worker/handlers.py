from datetime import datetime, timezone
from typing import Any

from app.application.dto.dto import ExtractedExperienceMessage
from app.core.enums import JobType
from app.domain.experience_extraction.processor import ExperienceExtractionProcessor
from app.domain.portfolio_strategy_generation.processor import PortfolioStrategyProcessor
from app.domain.interview_strategy_generation.processor import InterviewStrategyProcessor
from app.application.dto.dto import PortfolioStrategyGenerationMessage, ExtractedExperienceMessage, InterviewStrategyGenerationMessage

from typing import Union

JobMessage = Union[
    ExtractedExperienceMessage,
    PortfolioStrategyGenerationMessage,
    InterviewStrategyGenerationMessage
]

class JobHandler:
    # TODO : processor가 늘어날 때 마다 추가해주자
    def __init__(self, 
                 experience_processor: ExperienceExtractionProcessor, 
                 portfolio_strategy_processor: PortfolioStrategyProcessor,
                 interview_strategy_processor: InterviewStrategyProcessor
                 ) -> None:
        self.experience_processor = experience_processor
        self.portfolio_strategy_processor = portfolio_strategy_processor
        self.interview_strategy_processor = interview_strategy_processor

    # TODO : 여기서 job_type에 따라서 다른 처리를 할 수 있도록 해야 함.
    def handle(self, message: JobMessage) -> dict[str, Any]:
        if message.job_type == JobType.EXPERIENCE_EXTRACTION:
            result = self.experience_processor.process(message.file_asset_ids)
        elif message.job_type == JobType.PORTFOLIO_STRATEGY_GENERATION:
            result = self.portfolio_strategy_processor.process(message)
        elif message.job_type == JobType.INTERVIEW_STRATEGY_GENERATION:
            result = self.interview_strategy_processor.process(message)
        else:
            raise ValueError(f"Unsupported job type: {message.job_type}")

        print(f"Processed job {message.id} of type {message.job_type}. Result: {result}")
        return {
            "type" : message.job_type.value,
            "id" : message.id, # 각 테스크 마다 받아온 아이디 값
            "user_id": str(message.user_id),
            "status": "COMPLETED",
            "result": result,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
