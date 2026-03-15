from app.application.ports.ports import ExtractedExperienceRepositoryPort
from app.domain.experience_extraction.model import ExperienceExtraction
from sqlalchemy import select


"""
ExtractedExperienceRepositoryPort 인터페이스의 SQLAlchemy 구현체입니다
"""
class SqlAlchemyExtractedExperienceRepository(ExtractedExperienceRepositoryPort):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_extracted_experiences(self, extracted_experience_ids: list[int]) -> list[ExperienceExtraction]:
        with self.session_factory() as session:
            stmt = select(ExperienceExtraction).where(
                ExperienceExtraction.id.in_(extracted_experience_ids)
            )
            rows = session.scalars(stmt).all()

            if not rows:
                raise ValueError(
                    f"No extracted experience found for extracted_experience_ids: {extracted_experience_ids}"
                )

            return rows