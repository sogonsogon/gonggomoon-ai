from pydantic import BaseModel, Field

class PortfolioStrategyGenerationRequest(BaseModel):
    user_id: int = Field(description="포트폴리오 전략을 생성할 사용자 ID")
    portfolio_strategy_id: int = Field(description="API 서버가 생성한 포트폴리오 전략 생성 작업 ID")
    experiences: list[dict] = Field(description="포트폴리오 전략 생성을 위한 경험 데이터 리스트")
    job_type: str = Field(description="직무 유형 - 예: 'BACKEND'")
    industry_type: str = Field(description="산업 유형 - 예: 'TECH', 'FINANCE', 'HEALTHCARE' 등")