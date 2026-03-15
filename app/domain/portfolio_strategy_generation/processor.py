from typing import Any
from app.application.ports.ports import PortfolioStrategyGeneratorPort
from app.application.dto.dto import PortfolioStrategyGenerationMessage

class PortfolioStrategyProcessor:
    def __init__(
        self,
        generator: PortfolioStrategyGeneratorPort
    ):
        self.generator = generator

    def process(self, message: PortfolioStrategyGenerationMessage) -> dict[str, Any]:
        
        experiences = message.experiences
        position_type = message.position_type
        industry_type = message.industry_type

        # generator를 호출하여 포트폴리오 전략을 생성
        strategy_result = self.generator.generate(
            experiences=experiences,
            position_type=position_type,
            industry_type=industry_type
        )

        return strategy_result