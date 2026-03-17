from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import BigInteger, Text, DateTime, Enum as SAEnum


class PostStatus(str, Enum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    ANALYZED = "ANALYZED"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class JobType(str, Enum):
    FRONTEND = "FRONTEND"
    BACKEND = "BACKEND"
    EMBEDDED = "EMBEDDED"
    DEVOPS = "DEVPOS"
    DATA_ANALYSIS = "DATA_ANALYSIS"
    AI = "AI"
    INFORMATION_SECURITY = "INFORMATION_SECURITY"
    DESIGN = "DESIGN"
    PM_PO = "PM_PO"
    QA = "QA"


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )

    submission_id: Optional[int] = Field(
        default=None,
        sa_column=Column("submission_id", BigInteger, nullable=True)
    )

    company_id: int = Field(
        sa_column=Column("company_id", BigInteger, nullable=False)
    )

    platform_id: Optional[int] = Field(
        default=None,
        sa_column=Column("platform_id", BigInteger, nullable=True)
    )

    title: str = Field(
        sa_column=Column("title", nullable=False)
    )

    url: Optional[str] = Field(
        default=None,
        sa_column=Column("url", nullable=True)
    )

    experience_level: Optional[int] = Field(
        default=None,
        sa_column=Column("experience_level", nullable=True)
    )

    status: PostStatus = Field(
        sa_column=Column(
            "status",
            SAEnum(PostStatus, name="post_status"),
            nullable=False
        )
    )

    job_type: JobType = Field(
        sa_column=Column(
            "job_type",
            SAEnum(JobType, name="job_type"),
            nullable=False
        )
    )

    original_content: str = Field(
        sa_column=Column("original_content", Text, nullable=False)
    )

    started_at: datetime = Field(
        sa_column=Column("started_at", DateTime(timezone=True), nullable=False)
    )

    expired_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("expired_at", DateTime(timezone=True), nullable=True)
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("created_at", DateTime(timezone=True), nullable=False)
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("updated_at", DateTime(timezone=True), nullable=True)
    )

    analyzed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("analyzed_at", DateTime(timezone=True), nullable=True)
    )

    published_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("published_at", DateTime(timezone=True), nullable=True)
    )