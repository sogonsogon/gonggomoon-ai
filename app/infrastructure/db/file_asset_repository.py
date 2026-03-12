from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.application.ports.ports import FileAssetRepositoryPort
from app.infrastructure.db.models import FileAssetModel


class FileAssetNotFoundError(Exception):
    pass


class SqlAlchemyFileAssetRepository(FileAssetRepositoryPort):
    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory = session_factory

    def get_file_key(self, file_asset_id: int) -> str:
        with self.session_factory() as session:
            stmt = select(FileAssetModel.file_key).where(FileAssetModel.id == file_asset_id)
            file_key = session.execute(stmt).scalar_one_or_none()
            print(f"Queried file_key for file_asset_id {file_asset_id}: {file_key}")  # 디버깅용 로그

            if file_key is None:
                raise FileAssetNotFoundError(f"file asset not found: {file_asset_id}")

            return file_key