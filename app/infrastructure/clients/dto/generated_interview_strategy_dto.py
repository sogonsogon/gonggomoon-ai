from enum import StrEnum
from pydantic import BaseModel, Field


class QuestionLevel(StrEnum):
    HIGH = "HIGH"
    MIDDLE = "MIDDLE"
    LOWER = "LOWER"


class InterviewQuestion(BaseModel):
    question: str = Field(description="면접 질문")
    questionLevel: QuestionLevel = Field(description="질문 난이도")


class GeneratedInterviewStrategyPayload(BaseModel):
    questions: list[InterviewQuestion]
        