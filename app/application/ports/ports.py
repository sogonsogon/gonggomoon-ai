from typing import Any, Protocol

from app.application.dto.dto import ExtractedExperienceMessage


# JobQueuePort는 작업 메시지를 큐에 넣고 빼는 인터페이스를 정의합니다.
# TODO : ExtractedExperienceMessage 대신 좀 더 범용적인 JobMessage로 리팩토링하는 것을 고려해보자.
class JobQueuePort:
    def enqueue(self, message: ExtractedExperienceMessage) -> None:
        raise NotImplementedError

    def dequeue(self) -> ExtractedExperienceMessage | None:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class FileStorePort(Protocol):
    def download(self, file_asset_id: int) -> bytes:
        ...


class ExperienceAnalyzerPort(Protocol):
    def analyze(self, resume_text: str) -> dict[str, Any]:
        ...

class PortfolioStrategyGeneratorPort(Protocol):
    def generate(self, experiences: list[dict], position_type: str, industry_type: str) -> dict[str, Any]:
        ...

class InterviewStrategyGeneratorPort(Protocol):
    def generate(self, file_asset_id: int) -> dict[str, Any]:
        ...

class CallbackPort(Protocol):
    def send(self, callback_url: str, body: dict[str, Any]) -> None:
        ...

class PdfTextExtractorPort(Protocol):
    def extract_text(self, pdf_bytes: bytes) -> str:
        ...

class FileAssetRepositoryPort(Protocol):
    def get_file_key(self, file_asset_id: int) -> str:
        ...

class ExtractedExperienceRepositoryPort(Protocol):
    def get_extracted_experiences(self, extracted_experience_id: int) -> list[dict[str, Any]]:
        ...

class InterviewStrategyRepositoryPort(Protocol):
    def get_file_asset_id(self, interview_strategy_generation_message_id: int) -> int:
        ...

# Post analysis 관련 포트
class PostAnalyzerPort(Protocol):
    def analyze(self, company_name:str, company_description:str, post_content:str) -> dict[str, Any]:
        ...

class CompanyRepositoryPort(Protocol):
    def get_company_info(self, company_id: int) -> dict[str, Any]:
        ...

class PostRepositoryPort(Protocol):
    def get_post_info(self, post_id: int) -> dict[str, Any]:
        ...