import re

from backend.app.demos.sample_data import SIMULATED_PDF_PAGES
from backend.app.schemas import DemoResponse, DemoStep


def detect_section(text: str) -> str:
    lowered = text.lower()
    for section in ["abstract", "methods", "results", "discussion"]:
        if section in lowered:
            return section.title()
    return "Unknown"


def clean_text(text: str) -> str:
    compact = re.sub(r"\s+", " ", text)
    return compact.strip()


def run(question: str, options: dict) -> DemoResponse:
    parsed_pages = []
    for page in SIMULATED_PDF_PAGES:
        parsed_pages.append(
            {
                "page": page["page"],
                "section": detect_section(page["raw_text"]),
                "clean_text": clean_text(page["raw_text"]),
            }
        )

    return DemoResponse(
        demo_id="pdf_parsing",
        title="02 PDF Parsing",
        concept=(
            "PDF parsing converts page-level paper content into clean text while preserving "
            "page and section context for later citations."
        ),
        steps=[
            DemoStep(name="simulated_pdf_pages", output=SIMULATED_PDF_PAGES),
            DemoStep(name="cleaned_page_records", output=parsed_pages),
        ],
        final_output={
            "parsed_document": {
                "title": "Ultrasound-guided ablation monitoring",
                "pages": parsed_pages,
            }
        },
        interview_notes=[
            "PDF parsing quality controls the quality of every later RAG step.",
            "The key is to preserve page-level context, because citations need page support.",
        ],
    )

