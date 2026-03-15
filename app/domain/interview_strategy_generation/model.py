from __future__ import annotations

from datetime import date, datetime, timezone
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class InterviewStrategy(SQLModel, table=True):
    __tablename__ = "interview_strategy"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, index=True)
    file_asset_id: int = Field(nullable=False, index=True)

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )

    generated_date: date = Field(
        nullable=False,
    )