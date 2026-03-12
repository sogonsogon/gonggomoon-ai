from enum import StrEnum
from typing import List, Optional
from pydantic import BaseModel, Field

# extraction 전용 DTO로 두는 걸 추천
# (SQLModel 대신 BaseModel이 structured output에 더 안정적)
class ExperienceType(str):
    PROJECT = "PROJECT"
    CAREER = "CAREER"
    EDUCATION = "EDUCATION"
    COMPETITION = "COMPETITION"
    OTHER = "OTHER"


class ExtractedExperienceItem(BaseModel):
    title: str = Field(..., description="추출된 경험 제목")
    experienceContent: str = Field(..., description="추출된 경험 내용")
    experienceType: str = Field(
        ...,
        description="경험 타입. 반드시 PROJECT, CAREER, EDUCATION, COMPETITION, OTHER 중 하나",
    )
    startDate: str | None = Field(default=None, description="시작일, 예: 2024-03")
    endDate: str | None = Field(default=None, description="종료일, 예: 2024-04")


class ExtractedExperiencesPayload(BaseModel):
    experiences: list[ExtractedExperienceItem] = Field(
        default_factory=list,
        description="추출된 경험 목록",
    )