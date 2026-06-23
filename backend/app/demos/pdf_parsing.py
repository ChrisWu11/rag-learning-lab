from backend.app.demos.pdf_document import parse_sample_pdf
from backend.app.schemas import DemoResponse, DemoStep


def run(question: str, options: dict) -> DemoResponse:
    """Run the PDF parsing demo.

    Args:
        question: Included for API consistency; this demo focuses on page extraction.
        options: Reserved for future parser switches such as OCR on/off.
    """

    parsed = parse_sample_pdf()
    page_records = [
        {
            "page": page["page"],
            "section": page["section"],
            "clean_text": page["clean_text"],
        }
        for page in parsed["pages"]
    ]

    return DemoResponse(
        demo_id="pdf_parsing",
        title="02 PDF Parsing",
        concept=(
            "PDF parsing converts page-level paper content into clean text while preserving "
            "page and section context for later citations."
        ),
        steps=[
            DemoStep(name="pdf_file_info", output=parsed["pdf_info"]),
            DemoStep(name="extracted_page_text", output=parsed["pages"]),
            DemoStep(name="cleaned_page_records", output=page_records),
        ],
        final_output={
            "parsed_document": {
                **parsed["document_metadata"],
                "pages": page_records,
            }
        },
        interview_notes=[
            "PDF parsing quality controls the quality of every later RAG step.",
            "The key is to preserve page-level context, because citations need page support.",
        ],
    )
