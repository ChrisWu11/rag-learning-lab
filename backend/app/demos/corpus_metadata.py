from backend.app.demos.sample_data import paper_chunks
from backend.app.schemas import DemoResponse, DemoStep


def run(question: str, options: dict) -> DemoResponse:
    chunks = paper_chunks()
    citation_cards = [
        {
            "visible_label": f"[{index}]",
            "title": chunk["metadata"]["title"],
            "doi": chunk["metadata"]["doi"],
            "page": chunk["metadata"]["page"],
            "section": chunk["metadata"]["section"],
            "chunk_id": chunk["chunk_id"],
        }
        for index, chunk in enumerate(chunks, start=1)
    ]

    return DemoResponse(
        demo_id="corpus_metadata",
        title="01 Corpus & Metadata",
        concept=(
            "A private RAG corpus is not only text. Metadata such as DOI, page, "
            "section, and chunk ID makes answers auditable."
        ),
        steps=[
            DemoStep(name="raw_private_papers", output=chunks),
            DemoStep(name="citation_cards", output=citation_cards),
        ],
        final_output={
            "why_it_matters": [
                "Private papers can include institution-accessible content not visible to public chatbots.",
                "Page and section metadata lets the system show where an answer came from.",
                "Chunk IDs make retrieval and evaluation reproducible.",
            ]
        },
        interview_notes=[
            "I treated the knowledge base as structured evidence, not just plain text.",
            "Metadata is essential for citation support and debugging wrong answers.",
        ],
    )

