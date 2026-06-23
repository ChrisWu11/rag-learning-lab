import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader


SAMPLE_PDF_PATH = (
    Path(__file__).resolve().parents[1] / "sample_data" / "tiny_ablation_paper.pdf"
)
SECTION_NAMES = ["abstract", "methods", "results", "discussion", "limitations"]


def clean_text(text: str) -> str:
    """Collapse PDF extraction whitespace into readable text."""

    return re.sub(r"\s+", " ", text).strip()


def detect_section(text: str) -> str:
    """Detect the first known section heading present in a page of extracted text."""

    lowered = text.lower()
    for section in SECTION_NAMES:
        if re.search(rf"\b{section}\b", lowered):
            return section.title()
    return "Unknown"


def extract_metadata(first_page_text: str, page_count: int) -> dict[str, Any]:
    """Extract title, DOI, and year from the first PDF page.

    Args:
        first_page_text: Cleaned text from page 1.
        page_count: Number of pages reported by pypdf.
    """

    title_match = re.search(r"^(.*?)\s+DOI:", first_page_text)
    doi_match = re.search(r"DOI:\s*([^\s]+)", first_page_text)
    year_match = re.search(r"Year:\s*(\d{4})", first_page_text)
    return {
        "doc_id": "tiny_pdf_001",
        "title": title_match.group(1).strip() if title_match else "Unknown title",
        "doi": doi_match.group(1).strip() if doi_match else "Unknown DOI",
        "year": int(year_match.group(1)) if year_match else None,
        "source_type": "pdf",
        "source_path": str(SAMPLE_PDF_PATH),
        "page_count": page_count,
    }


def parse_sample_pdf() -> dict[str, Any]:
    """Read the committed tiny PDF and return metadata plus page-level text."""

    reader = PdfReader(str(SAMPLE_PDF_PATH))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        cleaned = clean_text(raw_text)
        pages.append(
            {
                "page": index,
                "section": detect_section(cleaned),
                "raw_text": raw_text,
                "clean_text": cleaned,
            }
        )

    first_page_text = pages[0]["clean_text"] if pages else ""
    metadata = extract_metadata(first_page_text, len(pages))
    return {
        "pdf_info": {
            "file_name": SAMPLE_PDF_PATH.name,
            "file_path": str(SAMPLE_PDF_PATH),
            "exists": SAMPLE_PDF_PATH.exists(),
            "size_bytes": SAMPLE_PDF_PATH.stat().st_size if SAMPLE_PDF_PATH.exists() else 0,
            "page_count": len(pages),
        },
        "document_metadata": metadata,
        "pages": pages,
    }


def parsed_pdf_text() -> str:
    """Join cleaned page text into one document string for chunking."""

    parsed = parse_sample_pdf()
    return "\n\n".join(page["clean_text"] for page in parsed["pages"])

