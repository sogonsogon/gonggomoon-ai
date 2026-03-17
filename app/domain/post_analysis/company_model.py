from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import BigInteger, Integer, Text, DateTime, Enum as SAEnum, String

class CompanyType(str, Enum):
    LARGE_ENTERPRISE = "LARGE_ENTERPRISE"
    MID_SIZED_ENTERPRISE = "MID_SIZED_ENTERPRISE"
    SMALL_MEDIUM_ENTERPRISE = "SMALL_MEDIUM_ENTERPRISE"
    STARTUP = "STARTUP"


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )

    industry_id: int = Field(
        sa_column=Column("industry_id", BigInteger, nullable=False)
    )

    name: str = Field(
        sa_column=Column("name", String, nullable=False)
    )

    type: CompanyType = Field(
        sa_column=Column(
            "type",
            SAEnum(CompanyType, name="company_type"),
            nullable=False
        )
    )

    employee_count: Optional[int] = Field(
        default=None,
        sa_column=Column("employee_count", Integer, nullable=True)
    )

    address: Optional[str] = Field(
        default=None,
        sa_column=Column("address", String, nullable=True)
    )

    description: Optional[str] = Field(
        default=None,
        sa_column=Column("description", Text, nullable=True)
    )

    founded_year: Optional[int] = Field(
        default=None,
        sa_column=Column("founded_year", Integer, nullable=True)
    )

    url: Optional[str] = Field(
        default=None,
        sa_column=Column("url", String, nullable=True)
    )

    created_by: int = Field(
        sa_column=Column("created_by", BigInteger, nullable=False)
    )

    updated_by: Optional[int] = Field(
        default=None,
        sa_column=Column("updated_by", BigInteger, nullable=True)
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("created_at", DateTime(timezone=True), nullable=False)
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("updated_at", DateTime(timezone=True), nullable=False)
    )