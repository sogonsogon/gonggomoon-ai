from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field

from enum import StrEnum

# 경험 추출 상태
class ExtractionStatus(StrEnum):
    READY = "READY"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"

# 경험 유형
class ExperienceType(StrEnum):
    PROJECT = "PROJECT"
    CAREER = "CAREER"
    EDUCATION = "EDUCATION"
    COMPETITION = "COMPETITION"
    OTHER = "OTHER"

# 추출된 경험 항목    
class ExtractedExperienceItem(SQLModel):
    title: str = Field(..., description="추출된 경험 제목")
    experienceContent: str = Field(..., description="추출된 경험 내용")
    experienceType: ExperienceType = Field(..., description="경험 타입")
    startDate: Optional[str] = Field(default=None, description="시작일, 예: 2024-03")
    endDate: Optional[str] = Field(default=None, description="종료일, 예: 2024-04")

# 추출된 경험 목록 페이로드
class ExtractedExperiencesPayload(SQLModel):
    experiences: List[ExtractedExperienceItem] = Field(
        default_factory=list,
        description="추출된 경험 목록",
    )


# extracted_experiences 테이블 모델
class ExperienceExtraction(SQLModel, table=True):
    __tablename__ = "extracted_experiences"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)
    file_asset_id: int = Field(nullable=False)
    status: ExtractionStatus = Field(default=ExtractionStatus.PROCESSING, nullable=False)

    # 추출된 경험 데이터는 JSONB 형태로 저장
    experiences: list[dict] | None = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
        description="추출된 경험 목록(JSONB)",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )