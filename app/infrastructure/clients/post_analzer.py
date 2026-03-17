from typing import Any
from app.application.ports.ports import PostAnalyzerPort
from google import genai
from google.genai import types
from app.infrastructure.clients.dto.post_analysis_dto import PostAnalysisPayload
import json

class GeminiPostAnalyzer(PostAnalyzerPort):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze(self, company_name:str, company_description:str, post_content:str) -> dict[str, Any]:
        print("log : Starting post analysis using GeminiPostAnalyzer")

        prompt = self._create_prompt(company_name, company_description, post_content)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema = PostAnalysisPayload,
                temperature=0,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()
        return PostAnalysisPayload.model_validate_json(response.text).model_dump()

    def _create_prompt(self, company_name: str, company_description: str, post_content: str) -> str:

        schema_text = json.dumps(
            PostAnalysisPayload.model_json_schema(),
            ensure_ascii=False,
            indent=2
        )
        prompt = f"""
            You analyze the job posting content and extract key information.

            Return JSON that MUST match the provided schema exactly.

            Company Name:
            {company_name}

            Company Description:
            {company_description}

            Job Posting Content:
            {post_content}

            Schema:
            {schema_text}

            Rules:
            - Output MUST be valid JSON
            - Output must contain ONLY the keys defined in the schema
            - All string values must be written in Korean
            - Do not include markdown, explanations, or extra keys

            Field rules:
            summary
            - Job title + experience requirement + company name
            - Maximum 20 Korean characters
            - If longer, rewrite to fit the limit

            company_intro
            - Company mission or domain inferred from the posting or company name
            - Maximum 30 Korean characters

            rnr
            - Extract responsibilities directly from the job posting
            - Maximum 5 items
            - Each item should be a short phrase

            required_skills
            - Extract required or preferred skills
            - Maximum 5 items

            differentiators
            - Preferred qualifications or hidden priorities inferred from the posting
            - Maximum 3 items
            - Do not invent information not implied in the text

            hidden_keywords
            - Domain, job, or skill focused hashtags
            - Maximum 5 items
            - Each item must start with "#"

            action_items
            - Immediate preparation steps before applying
            - Maximum 3 items
            
        """

        return prompt