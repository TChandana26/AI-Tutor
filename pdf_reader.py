import fitz  

def is_image_based_pdf(filepath: str) -> bool:
    """
    Check if a PDF is image-based (scanned) with no extractable text.
    Returns True if image-based, False if text-based.
    """
    doc        = fitz.open(filepath)
    total_text = ""

    for page in doc:
        total_text += page.get_text().strip()

    doc.close()

    # If less than 50 characters extracted across whole PDF, it's likely image-based
    return len(total_text) < 50


def extract_text(filepath: str) -> tuple[str, int]:
    """
    Open a PDF and extract all text content.
    Raises ValueError if PDF is image-based (scanned).
    Returns: (full_text, total_pages)
    """
    if is_image_based_pdf(filepath):
        raise ValueError(
            "IMAGE_BASED_PDF: This PDF appears to be scanned or image-based. "
            "Please upload a text-based PDF instead."
        )

    doc   = fitz.open(filepath)
    pages = len(doc)
    text  = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text.strip(), pages


def extract_by_page(filepath: str) -> list[dict]:
    """
    Extract text page by page (useful for large PDFs).
    Returns: list of { page_num, text }
    """
    doc   = fitz.open(filepath)
    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "page_num": i + 1,
            "text":     page.get_text().strip()
        })

    doc.close()
    return pages