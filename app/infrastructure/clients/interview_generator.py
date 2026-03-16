from app.application.ports.ports import InterviewStrategyGeneratorPort
from google import genai
from google.genai import types
from app.infrastructure.clients.dto.generated_interview_strategy_dto import GeneratedInterviewStrategyPayload, InterviewQuestion

class GeminiInterviewStrategyGenerator(InterviewStrategyGeneratorPort):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self,
        resume_text: str,
    ) -> GeneratedInterviewStrategyPayload:
        print("log : Starting interview strategy generation using InterviewStrategyGenerator")

        prompt = self._create_prompt(resume_text)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeneratedInterviewStrategyPayload,
                temperature=0,
            ),
        )

        if response.parsed is not None:
            return response.parsed.model_dump()

        return GeneratedInterviewStrategyPayload.model_validate_json(response.text).model_dump()

    def _create_prompt(self, resume_text: str) -> str:
        
        # TODO : 나중에 타겟 기업 정보를 넣어서 생성하는 것도 좋아보임
        prompt = f"""
            You generate interview question data from resume text.

            Return JSON that MUST match the provided schema exactly.

            Rules:
            - Output must contain only one top-level key: "questions"
            - All string values must be written in Korean
            - Do not include markdown, code fences, explanations, or extra keys
            - Generate 5 interview questions
            - Questions must not exceed 200 characters
            - Each question must be based on the user's actual resume content
            - Prefer questions that deeply examine the user's real experiences, decisions, trade-offs, problem solving, and technical understanding
            - Avoid duplicate or overly similar questions
            - Each question should be clear, specific, and realistic for an actual interview
            - questionLevel must be one of: HIGH, MIDDLE, LOWER
            - HIGH means deep technical reasoning, architecture, trade-off, or problem-solving questions
            - MIDDLE means implementation, design choice, collaboration, or practical experience questions
            - LOWER means basic concept confirmation or introductory experience questions
            - Include a balanced mix of difficulty levels when possible
            - Focus on the most important and distinctive experiences, projects, technologies, and achievements in the resume

            Resume Text:
            {resume_text}
        """

        return prompt