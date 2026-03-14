from app.core.config import get_settings
from app.domain.experience_extraction.processor import ExperienceExtractionProcessor
from app.infrastructure.clients.callback_client import HttpCallbackClient
from app.infrastructure.clients.file_store import S3FileStore
from app.infrastructure.clients.llm_analyzer import GeminiExperienceAnalyzer
from app.infrastructure.queue.redis_queue import RedisJobQueue
from app.worker.executor import WorkerExecutor
from app.worker.handlers import JobHandler
from app.infrastructure.pdf.pdf_text_extractor import PyMuPdfTextExtractor
from app.infrastructure.db.session import create_session_factory
from app.infrastructure.db.file_asset_repository import SqlAlchemyFileAssetRepository
from app.infrastructure.db.extracted_experience_repository import SqlAlchemyExtractedExperienceRepository
from app.application.services.experiece_extraction_service import ExperienceExtractionService
from app.application.services.portfolio_strategy_generation_service import PortfolioStrategyGenerationService

settings = get_settings()
session_factory = create_session_factory(settings.database_url)

##### API 서버 관련 의존성 주입 ######
queue = RedisJobQueue(
    redis_url=settings.redis_url,
    queue_key=settings.redis_queue_key,
)

extracted_experience_repository = SqlAlchemyExtractedExperienceRepository(session_factory=session_factory)

experience_extraction_service = ExperienceExtractionService(
    queue=queue, 
    repository=extracted_experience_repository,
    callback_url=settings.call_back_url + "/experience-extraction"
)

portfolio_strategy_generation_service = PortfolioStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/portfolio-strategy-generation"
)


###### Worker 관련 의존성 주입 ######
# S3 파일 스토어 클라이언트 (PDF 파일을 저장하고 읽어오는 역할)
file_store = (
    S3FileStore(
        bucket=settings.s3_bucket,
        region=settings.s3_region,
    )
    if settings.s3_bucket
    else Exception("S3 버킷 정보가 설정되어 있지 않습니다.")
)

file_asset_repository = SqlAlchemyFileAssetRepository(session_factory=session_factory)


text_extractor = PyMuPdfTextExtractor()

analyzer = (
    GeminiExperienceAnalyzer(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    if settings.gemini_api_key
    else Exception("Gemini API 키가 설정되어 있지 않습니다.")
)

# 경험 추출 프로세서 (pdf에서 경험을 추출하는 핵심 비즈니스 로직 담당)
experience_processor = ExperienceExtractionProcessor(
    file_store=file_store,
    analyzer=analyzer,
    text_extractor=text_extractor,
    file_asset_repository=file_asset_repository
)

job_handler = JobHandler(experience_processor=experience_processor)
worker_executor = WorkerExecutor(
    queue=queue,
    handler=job_handler,
    callback_client=HttpCallbackClient(),
)
