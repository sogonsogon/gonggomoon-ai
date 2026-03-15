from app.application.ports.ports import JobQueuePort
from app.api.dto.portfolio_strategy_generation import PortfolioStrategyGenerationRequest
from app.application.dto.dto import PortfolioStrategyGenerationMessage

class PortfolioStrategyGenerationService:
    def __init__(self, queue: JobQueuePort, callback_url: str | None) -> None:
        self.queue = queue
        self.callback_url = callback_url

    def enqueue_portfolio_strategy_generation(self, request: PortfolioStrategyGenerationRequest) -> None:
        
        # JonMessage 생성
        message = PortfolioStrategyGenerationMessage(
            user_id=request.user_id,
            id=request.portfolio_strategy_id,
            experiences=request.experiences,
            position_type=request.position_type,
            industry_type=request.industry_type,
            callback_url=self.callback_url
        )


        # 큐에 메시지 넣기
        self.queue.enqueue(message)