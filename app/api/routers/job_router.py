# API 서버에서 AI 서버로 작업 제출 및 상태 조회를 위한 라우터

from fastapi import APIRouter, Header, status
from app.api.dependencies.auth import verify_internal_api_key
from app.api.dto.experience_extraction import ExperienceExtractionRequest
from app.api.dto.portfolio_strategy_generation import PortfolioStrategyGenerationRequest
from app.api.dto.interview_strategy_generation import InterviewStrategyGenerationRequest
from app.api.dto.post_analysis_request import PostAnalysisRequest
from app.application.container import queue, experience_extraction_service, portfolio_strategy_generation_service, interview_strategy_generation_service, post_analysis_service

jobs_router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

# {host}/api/v1/jobs/experience-extraction 엔드포인트로 POST 요청이 들어오면 작업 제출 처리
# 응답 값은 없고, 작업이 정상적으로 큐에 제출되면 202 Accepted 상태 코드만 반환함.
@jobs_router.post("/experience-extraction", response_model=None, status_code=status.HTTP_202_ACCEPTED)
def extract_experience(
    request: ExperienceExtractionRequest,
    x_internal_api_key: str | None = Header(default=None),
) -> None:
    # 내부 API 키 검증 - 외부에서 접근 불가능하도록 보안 강화
    # 근데 지금 당장 필요한지 모르겠음.
    verify_internal_api_key(x_internal_api_key)

    # 작업 제출 서비스 호출 - 작업 메시지를 큐에 넣고 응답 반환
    # 실제 작업 처리는 백그라운드에서 워커가 담당하므로, API는 즉시 응답을 반환함.
    return experience_extraction_service.enqueue_experience_extraction(request)

@jobs_router.post("/portfolio-strategy-generation", response_model=None, status_code=status.HTTP_202_ACCEPTED)
def generate_portfolio_strategy(
    request: PortfolioStrategyGenerationRequest,
    x_internal_api_key: str | None = Header(default=None),
) -> None:
    verify_internal_api_key(x_internal_api_key)
    return portfolio_strategy_generation_service.enqueue_portfolio_strategy_generation(request)

@jobs_router.post("/interview-strategy-generation", response_model=None, status_code=status.HTTP_202_ACCEPTED)
def generate_interview_strategy(
    request: InterviewStrategyGenerationRequest,
    x_internal_api_key: str | None = Header(default=None),
) -> None:
    verify_internal_api_key(x_internal_api_key)
    return interview_strategy_generation_service.enqueue_interview_strategy_generation(request)

@jobs_router.post("/post-analysis", response_model=None, status_code=status.HTTP_202_ACCEPTED)
def analyze_post(
    request: PostAnalysisRequest,
    x_internal_api_key: str | None = Header(default=None),
) -> None:
    verify_internal_api_key(x_internal_api_key)
    return post_analysis_service.enqueue_post_analysis(request)

# 큐에 쌓인 작업 수를 조회하는 엔드포인트 - AI 서버에서 작업 처리 상태 모니터링 용도
# 지금 굳이 필요한가 싶음
@jobs_router.get("/queue-size", status_code=status.HTTP_200_OK)
def get_queue_size(
    x_internal_api_key: str | None = Header(default=None),
) -> dict[str, int]:
    verify_internal_api_key(x_internal_api_key)
    return {"queue_size": queue.size()}
