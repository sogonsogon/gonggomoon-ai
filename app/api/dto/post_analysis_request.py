from pydantic import BaseModel, Field

class PostAnalysisRequest(BaseModel):
    post_id: int = Field(description="분석할 게시글의 ID")
    user_id: int = Field(description="게시글 작성자의 사용자 ID, 현재는 관리자 1명")