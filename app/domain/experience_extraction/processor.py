from typing import Any

from app.application.ports.ports import ExperienceAnalyzerPort, FileStorePort, PdfTextExtractorPort
from app.domain.experience_extraction.policies import validate_pdf_bytes
from app.application.ports.ports import FileAssetRepositoryPort

# ExperienceExtractionProcessor는 PDF 파일에서 경험을 추출하는 핵심 비즈니스 로직을 담당합니다.  
class ExperienceExtractionProcessor:
    def __init__(
        self,
        file_store: FileStorePort,
        text_extractor: PdfTextExtractorPort,
        analyzer: ExperienceAnalyzerPort,
        file_asset_repository: FileAssetRepositoryPort
    ) -> None:
        self.file_store = file_store
        self.text_extractor = text_extractor
        self.analyzer = analyzer
        self.file_asset_repository = file_asset_repository

    def process(self, file_asset_id: int) -> dict[str, Any]:
        # 여기서 file_asset_id로 DB에서 Key값을 조회해와야 함.
        file_key = self.file_asset_repository.get_file_key(file_asset_id)

        # S3에서 PDF를 다운로드 해온다.
        pdf_bytes = self.file_store.download(file_key)
        validate_pdf_bytes(pdf_bytes)

        # PDF에서 텍스트를 추출한다.
        resume_text = self.text_extractor.extract_text(pdf_bytes)

        # 추출된 텍스트를 분석하여 경험을 추출한다.
        return self.analyzer.analyze(resume_text)
