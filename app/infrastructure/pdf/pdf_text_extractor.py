from app.application.ports.ports import PdfTextExtractorPort
import fitz  # PyMuPDF

# PyMuPDF를 사용하여 PDF에서 텍스트를 추출하는 구현체입니다.
class PyMuPdfTextExtractor(PdfTextExtractorPort):
    def __init__(self, max_pages: int | None = None) -> None:
        self.max_pages = max_pages

    def extract_text(self, pdf_bytes: bytes) -> str:
        if not pdf_bytes:
            raise ValueError("빈 PDF 데이터입니다.")

        texts: list[str] = []

        # PyMuPDF는 stream=bytes 로 문서를 열 수 있음
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            if doc.page_count == 0:
                raise ValueError("페이지가 없는 PDF입니다.")

            page_count = doc.page_count
            if self.max_pages is not None:
                page_count = min(page_count, self.max_pages)

            for page_index in range(page_count):
                page = doc.load_page(page_index)

                # sort=True: top-left -> bottom-right 기준으로 정렬된 텍스트 추출
                page_text = page.get_text("text", sort=True).strip()

                if page_text:
                    texts.append(
                        f"[PAGE {page_index + 1}]\n{page_text}"
                    )

        extracted = "\n\n".join(texts).strip()

        if not extracted:
            raise ValueError("PDF에서 추출된 텍스트가 없습니다. 스캔본이면 OCR이 필요할 수 있습니다.")

        return extracted