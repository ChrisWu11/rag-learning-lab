from typing import Any

from backend.app.demos.pdf_document import parse_sample_pdf
from backend.app.schemas import DemoResponse, DemoStep


def make_chunks(text: str, chunk_size: int, overlap: int) -> list[dict]:
    """Split text into overlapping character chunks.

    Args:
        text: Source document text to split.
        chunk_size: Maximum number of characters in each chunk.
        overlap: Number of characters repeated between adjacent chunks.
    """

    chunks = []
    start = 0
    index = 1
    step = max(1, chunk_size - overlap)
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(
            {
                "chunk_index": index,
                "start_char": start,
                "end_char": end,
                "content": text[start:end],
            }
        )
        if end == len(text):
            break
        start += step
        index += 1
    return chunks


def pdf_text_with_page_spans(parsed: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """Join PDF pages and keep character spans for page/section metadata.

    Args:
        parsed: Output from parse_sample_pdf().
    """

    text_parts = []
    spans = []
    cursor = 0
    for page in parsed["pages"]:
        page_text = page["clean_text"]
        text_parts.append(page_text)
        start = cursor
        end = start + len(page_text)
        spans.append(
            {
                "page": page["page"],
                "section": page["section"],
                "start_char": start,
                "end_char": end,
            }
        )
        cursor = end + 2
    return "\n\n".join(text_parts), spans


def overlapping_page_metadata(chunk: dict, page_spans: list[dict[str, Any]]) -> dict[str, Any]:
    """Return PDF pages and sections touched by a chunk character span."""

    touched = [
        span
        for span in page_spans
        if chunk["start_char"] < span["end_char"] and chunk["end_char"] > span["start_char"]
    ]
    return {
        "pages": [span["page"] for span in touched],
        "sections": [span["section"] for span in touched],
    }


def run(question: str, options: dict) -> DemoResponse:
    """Run the chunking demo.

    Args:
        question: Included for API consistency; this demo focuses on text splitting.
        options: Supports chunk_size and overlap from the frontend controls.
    """

    chunk_size = int(options.get("chunk_size", 180))
    overlap = int(options.get("overlap", 40))
    parsed = parse_sample_pdf()
    metadata = parsed["document_metadata"]
    text, page_spans = pdf_text_with_page_spans(parsed)
    chunks = make_chunks(text, chunk_size=chunk_size, overlap=overlap)
    enriched = [
        {
            "chunk_id": f"{metadata['doc_id']}_c{chunk['chunk_index']:03d}",
            **chunk,
            "metadata": {
                "title": metadata["title"],
                "doi": metadata["doi"],
                "year": metadata["year"],
                "source_path": metadata["source_path"],
                "page_count": metadata["page_count"],
                **overlapping_page_metadata(chunk, page_spans),
            },
        }
        for chunk in chunks
    ]

    return DemoResponse(
        demo_id="chunking",
        title="03 Chunking",
        concept=(
            "Chunking turns long papers into retrieval units. Chunk size controls how much "
            "context each unit contains; overlap reduces boundary information loss."
        ),
        steps=[
            DemoStep(name="parsed_pdf_metadata", output=metadata),
            DemoStep(name="page_character_spans", output=page_spans),
            DemoStep(name="source_text", output=text),
            DemoStep(name="chunking_options", output={"chunk_size": chunk_size, "overlap": overlap}),
            DemoStep(name="chunks_with_metadata", output=enriched),
        ],
        final_output={
            "chunk_count": len(enriched),
            "tradeoff": "Smaller chunks retrieve precisely; larger chunks preserve context.",
        },
        interview_notes=[
            "I tuned chunk size and overlap because retrieval operates on chunks, not whole papers.",
            "Overlap protects information near chunk boundaries, but too much overlap adds duplicate evidence.",
        ],
    )
