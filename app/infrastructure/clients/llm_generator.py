from datetime import datetime, timezone
from typing import Any
from app.application.ports.ports import PortfolioStrategyGeneratorPort
from google import genai
from google.genai import types
from app.infrastructure.clients.dto.generated_portfolio_strategy_dto import GeneratedPortfolioStrategyPayload

class GeminiPortfolioStrategyGenerator(PortfolioStrategyGeneratorPort):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self,
        experiences: list[dict],
        position_type: str,
        industry_type: str
    ) -> GeneratedPortfolioStrategyPayload:
        print("log : Starting portfolio strategy generation using PortfolioStrategyGenerator")

        prompt = self._create_prompt(experiences, position_type, industry_type)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeneratedPortfolioStrategyPayload,
                temperature=0,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return GeneratedPortfolioStrategyPayload.model_validate_json(response.text).model_dump()

    def _create_prompt(self, experiences: list[dict], position_type: str, industry_type: str) -> str:
        experience_str = "\n\n".join(
            [
                (
                    f"Title: {exp['title']} [{exp['experienceType']}] "
                    f"({exp['startDate']} - {exp['endDate']})\n"
                    f"- ImpactTier: {exp['impactTier']}\n"
                    f"- TeamSize: {exp['teamSize']}\n"
                    f"- Role: {exp['roleType']}\n"
                    f"- Experience Content:\n{exp['experienceContent']}"
                )
                for exp in experiences
            ]
        )

        prompt = f"""
            You generate portfolio strategy data from experience data.

            Return JSON that MUST match the provided schema exactly.

            Rules:
            - Output must contain only one top-level key: "portfolioStrategy"
            - All string values must be written in Korean
            - Do not include markdown, code fences, or explanations
            - experienceType must be one of: PROJECT, CAREER, EDUCATION, COMPETITION, OTHER
            - experienceOrdering means the priority order in which the user's experiences should appear in the portfolio, based on the target position and industry the user is aiming for
            - experienceOrdering.order must start from 1 and increase sequentially without gaps
            - experienceStrategyPoints must reference only experiences that exist in the input data
            - experienceOrdering.title must exactly match an input experience title
            - keywords, strengths, and kpiCheckList should be concise and practical
            - improvementGuides should contain actionable advice

            Target:
            - positionType: {position_type}
            - industryType: {industry_type}

            Experience Data:
            {experience_str}
        """
        return prompt

    # def _parse_response(self, response: str) -> dict[str, Any]:
    #     # LLM의 응답을 파싱하여 필요한 정보를 추출
    #     # 예시에서는 간단히 JSON 형태로 응답이 온다고 가정
    #     try:
    #         return json.loads(response)
    #     except json.JSONDecodeError:
    #         raise ValueError("Invalid response format from LLM")