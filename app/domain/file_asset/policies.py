def validate_pdf_bytes(pdf_bytes: bytes) -> None:
    if not pdf_bytes:
        raise ValueError("Empty PDF content.")
