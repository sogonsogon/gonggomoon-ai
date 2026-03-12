from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String


class Base(DeclarativeBase):
    pass


class FileAssetModel(Base):
    __tablename__ = "file_asset"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file_key: Mapped[str] = mapped_column(String(512), nullable=False)