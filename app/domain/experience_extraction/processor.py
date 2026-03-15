from typing import Any

from app.application.ports.ports import ExperienceAnalyzerPort, FileStorePort, PdfTextExtractorPort
from app.domain.file_asset.policies import validate_pdf_bytes
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

    def process(self, file_asset_ids: list[dict[str,int]]) -> list[dict[str, Any]]:
        results = []

        for file_asset_id in file_asset_ids:
            file_key = self.file_asset_repository.get_file_key(file_asset_id["file_asset_id"])

            pdf_bytes = self.file_store.download(file_key)
            validate_pdf_bytes(pdf_bytes)

            resume_text = self.text_extractor.extract_text(pdf_bytes)

            result = self.analyzer.analyze(resume_text)
            results.append({
                "extracted_experience_id": file_asset_id["extracted_experience_id"],
                "file_asset_id": file_asset_id["file_asset_id"],
                "result": result,
            })

        return results
