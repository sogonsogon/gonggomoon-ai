from app.core.config import get_settings
from app.domain.experience_extraction.processor import ExperienceExtractionProcessor
from app.domain.portfolio_strategy_generation.processor import PortfolioStrategyProcessor
from app.domain.interview_strategy_generation.processor import InterviewStrategyProcessor
from app.domain.post_analysis.processor import PostAnalysisProcessor
from app.infrastructure.clients.callback_client import HttpCallbackClient
from app.infrastructure.clients.file_store import S3FileStore
from app.infrastructure.clients.llm_analyzer import GeminiExperienceAnalyzer
from app.infrastructure.clients.llm_generator import GeminiPortfolioStrategyGenerator
from app.infrastructure.clients.interview_generator import GeminiInterviewStrategyGenerator
from app.infrastructure.clients.post_analzer import GeminiPostAnalyzer
from app.infrastructure.queue.redis_queue import RedisJobQueue
from app.worker.executor import WorkerExecutor
from app.worker.handlers import JobHandler
from app.infrastructure.pdf.pdf_text_extractor import PyMuPdfTextExtractor
from app.infrastructure.db.session import create_session_factory
from app.infrastructure.db.file_asset_repository import SqlAlchemyFileAssetRepository
from app.infrastructure.db.interview_strategy_repository import SqlAlchemyInterviewStrategyRepository
from app.infrastructure.db.extracted_experience_repository import SqlAlchemyExtractedExperienceRepository
from app.infrastructure.db.post_repository import SqlAlchemyPostRepository
from app.infrastructure.db.company_repository import SqlAlchemyCompanyRepository
from app.application.services.experiece_extraction_service import ExperienceExtractionService
from app.application.services.portfolio_strategy_generation_service import PortfolioStrategyGenerationService
from app.application.services.interview_strategy_generation_service import InterviewStrategyGenerationService
from app.application.services.post_analysis_service import PostAnalysisService

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

interview_strategy_generation_service = InterviewStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/interview-strategy-generation"
)

# NOTE : Post Analysis Service는 백오피스에서 사용할 예정이므로, 콜백 URL이 다릅니다.
post_analysis_service = PostAnalysisService(
    queue=queue,
    callback_url=settings.backoffice_callback_url + "/post-analysis"
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
interview_strategy_repository = SqlAlchemyInterviewStrategyRepository(session_factory=session_factory)
company_repository =  SqlAlchemyCompanyRepository(session_factory=session_factory)
post_repository = SqlAlchemyPostRepository(session_factory=session_factory)



text_extractor = PyMuPdfTextExtractor()

experience_analyzer = (
    GeminiExperienceAnalyzer(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    if settings.gemini_api_key
    else Exception("Gemini API 키가 설정되어 있지 않습니다.")
)

portfolio_generator = (
    GeminiPortfolioStrategyGenerator(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    if settings.gemini_api_key
    else Exception("Gemini API 키가 설정되어 있지 않습니다.")
)

interview_generator = (
    GeminiInterviewStrategyGenerator(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    if settings.gemini_api_key
    else Exception("Gemini API 키가 설정되어 있지 않습니다.")
)

post_analyzer = (
    GeminiPostAnalyzer(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    if settings.gemini_api_key
    else Exception("Gemini API 키가 설정되어 있지 않습니다.")
)

# 경험 추출 프로세서 (pdf에서 경험을 추출하는 핵심 비즈니스 로직 담당)
experience_processor = ExperienceExtractionProcessor(
    file_store=file_store,
    analyzer=experience_analyzer,
    text_extractor=text_extractor,
    file_asset_repository=file_asset_repository
)

# 포트폴리오 전략 생성 프로세서 (경험 데이터를 바탕으로 포트폴리오 전략을 생성하는 핵심 비즈니스 로직 담당)
portfolio_strategy_processor = PortfolioStrategyProcessor(
    generator=portfolio_generator
)

# 면접 전략 생성 프로세서 (이력서 데이터를 바탕으로 면접 전략을 생성하는 핵심 비즈니스 로직 담당)
interview_strategy_processor = InterviewStrategyProcessor(
    file_storage=file_store,
    text_extractor=text_extractor,
    file_asset_repository=file_asset_repository,
    interview_strategy_repository=interview_strategy_repository,
    generator=interview_generator
)

# 공고 분석 프로세서
post_analysis_processor = PostAnalysisProcessor(
    post_analyzer=post_analyzer,
    company_repository= company_repository,
    post_repository= post_repository,
)

job_handler = JobHandler(
    experience_processor=experience_processor,
    portfolio_strategy_processor=portfolio_strategy_processor,
    interview_strategy_processor=interview_strategy_processor,
    post_analysis_processor=post_analysis_processor
)


worker_executor = WorkerExecutor(
    queue=queue,
    handler=job_handler,
    callback_client=HttpCallbackClient(),
)
