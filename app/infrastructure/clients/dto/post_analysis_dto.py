from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, Field


class PostAnalysisPayload(BaseModel):
    summary: Annotated[str, Field(max_length=20)]
    company_intro: Annotated[str, Field(max_length=30)]

    rnr: Annotated[List[str], Field(max_length=5)]
    required_skills: Annotated[List[str], Field(max_length=5)]
    differentiators: Annotated[List[str], Field(max_length=3)]
    hidden_keywords: Annotated[List[str], Field(max_length=5)]
    action_items: Annotated[List[str], Field(max_length=3)]