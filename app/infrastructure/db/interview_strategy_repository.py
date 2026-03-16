from sqlalchemy.orm import Session
from sqlalchemy import select

from app.application.ports.ports import InterviewStrategyRepositoryPort
from app.domain.interview_strategy_generation.model import InterviewStrategy


class SqlAlchemyInterviewStrategyRepository(InterviewStrategyRepositoryPort):
    def __init__(self, session_factory: Session):
        self.session_factory = session_factory

    def get_file_asset_id(self, interview_strategy_id: int) -> int:
        with self.session_factory() as session:
            stmt = select(InterviewStrategy.file_asset_id).where(
                InterviewStrategy.id == interview_strategy_id
            )
            result = session.execute(stmt).scalar_one_or_none()

        if result is None:
            raise ValueError(
                f"No file_asset_id found for interview_strategy_id: {interview_strategy_id}"
            )

        return result