from app.application.ports.ports import ExtractedExperienceRepositoryPort
from app.domain.experience_extraction.model import ExperienceExtraction
from sqlalchemy import select


"""
ExtractedExperienceRepositoryPort 인터페이스의 SQLAlchemy 구현체입니다
"""
class SqlAlchemyExtractedExperienceRepository(ExtractedExperienceRepositoryPort):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_extracted_experience(self, extracted_experience_id: int) -> ExperienceExtraction:
        with self.session_factory() as session:
            stmt = select(ExperienceExtraction).where(
                ExperienceExtraction.id == extracted_experience_id
            )
            row = session.scalar(stmt)
    
            if row is None:
                raise ValueError(
                    f"No extracted experience found for extracted_experience_id: {extracted_experience_id}"
                )

            return ExperienceExtraction(
                id=row.id,
                user_id=row.user_id,
                file_asset_id=row.file_asset_id,
                status=row.status,
                experiences=row.experiences,
            )