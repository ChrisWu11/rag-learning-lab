from backend.app.demos.pdf_document import parse_sample_pdf
from backend.app.schemas import DemoResponse, DemoStep


def run(question: str, options: dict) -> DemoResponse:
    """Run the corpus metadata demo.

    Args:
        question: Included for API consistency; this demo inspects stored evidence.
        options: Reserved for future metadata filters such as year or section.
    """

    parsed = parse_sample_pdf()
    metadata = parsed["document_metadata"]
    citation_cards = [
        {
            "visible_label": f"[{page['page']}]",
            "title": metadata["title"],
            "doi": metadata["doi"],
            "year": metadata["year"],
            "page": page["page"],
            "section": page["section"],
            "source_type": metadata["source_type"],
            "source_path": metadata["source_path"],
        }
        for page in parsed["pages"]
    ]

    return DemoResponse(
        demo_id="corpus_metadata",
        title="01 Corpus & Metadata",
        concept=(
            "A private RAG corpus is not only text. Metadata such as DOI, page, "
            "section, and chunk ID makes answers auditable."
        ),
        steps=[
            DemoStep(name="pdf_file_info", output=parsed["pdf_info"]),
            DemoStep(name="extracted_document_metadata", output=metadata),
            DemoStep(name="citation_cards", output=citation_cards),
        ],
        final_output={
            "why_it_matters": [
                "Private papers can include institution-accessible content not visible to public chatbots.",
                "Page and section metadata lets the system show where an answer came from.",
                "The same parsed metadata can be copied onto chunks during ingestion.",
            ]
        },
        interview_notes=[
            "I treated the knowledge base as structured evidence, not just plain text.",
            "Metadata is essential for citation support and debugging wrong answers.",
        ],
    )
