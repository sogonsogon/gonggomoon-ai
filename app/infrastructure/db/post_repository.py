from app.application.ports.ports import PostRepositoryPort
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.domain.post_analysis.post_model import Post

class SqlAlchemyPostRepository(PostRepositoryPort):
    def __init__(self, session_factory:Session):
        self.session_factory = session_factory

    def get_post_info(self, post_id: int) -> Optional[Post]:
        with self.session_factory() as session:  # session_factory가 callable일 때
            statement = select(Post).where(Post.id == post_id)
            post = session.execute(statement).first()
            
            if post is None:
                raise ValueError(f"Post not found: {post_id}")  
            
            return dict(post._mapping)