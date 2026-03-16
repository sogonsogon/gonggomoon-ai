from datetime import datetime, timezone
import json
from typing import Any

from google import genai
from google.genai import types

from app.application.ports.ports import ExperienceAnalyzerPort
from app.infrastructure.clients.dto.extract_experience_dto import ExtractedExperiencesPayload


class GeminiExperienceAnalyzer(ExperienceAnalyzerPort):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze(self, resume_text: str) -> dict[str, Any]:
        print("log : Starting experience analysis using GeminiExperienceAnalyzer")

        prompt = f"""
            You extract structured experience data from resume text.

            Return JSON that MUST match the provided schema exactly.

            Rules:
            - Output must contain only one top-level key: "experiences"
            - experienceType must be one of: PROJECT, CAREER, EDUCATION, COMPETITION, OTHER
            - If a date is unknown, use null
            - Prefer YYYY-MM format for dates
            - startDate and endDate must be either:
                - null
                - or a string in yyyy-MM format
            - Do not output year-only values like "2025".
            - All string values must be written in Korean
            - Keep experienceType values exactly as enum values: PROJECT, CAREER, EDUCATION, COMPETITION, OTHER
            - You can extract experience from up to 10 target experiences.
            - Experiences should not be duplicated, and if there are no experiences to extract, you don't have to extract them.

            resume_text:
            {resume_text}
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedExperiencesPayload,
                temperature=0,
            ),
        )


        raw = response.text
        if not raw:
            raise ValueError("Gemini 응답 본문이 비어 있습니다.")

        try:
            validated = ExtractedExperiencesPayload.model_validate_json(raw)
        except Exception as e:
            raise ValueError(f"Gemini structured output 파싱 실패: raw={raw}") from e

        return {
            "model": self.model,
            "analysis": validated.model_dump(),
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }