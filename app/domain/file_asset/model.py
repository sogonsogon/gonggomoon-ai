from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional

from sqlmodel import SQLModel, Field


class DocumentCategory(StrEnum):
    PORTFOLIO = "PORTFOLIO"
    RESUME = "RESUME"
    OTHER = "OTHER"


class FileAssetStatus(StrEnum):
    UPLOADED = "UPLOADED", # 파일 업로드가 정상적으로 완료된 상태
    FAILED = "FAILED", # 파일 업로드 또는 처리 과정에서 오류가 발생한 상태
    DELETED = "DELETED" # 파일이 삭제된 상태


class FileAsset(SQLModel, table=True):
    __tablename__ = "file_asset"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)

    category: DocumentCategory = Field(
        sa_column_kwargs={"name": "document_category"},
        nullable=False,
    )

    status: FileAssetStatus = Field(nullable=False)

    original_file_name: str = Field(
        nullable=False,
        max_length=255,
    )

    file_key: str = Field(
        nullable=False,
        max_length=500,
    )

    size_bytes: int = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )