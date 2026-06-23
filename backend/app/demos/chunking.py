from backend.app.demos.sample_data import TOY_PAPERS
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


def run(question: str, options: dict) -> DemoResponse:
    """Run the chunking demo.

    Args:
        question: Included for API consistency; this demo focuses on text splitting.
        options: Supports chunk_size and overlap from the frontend controls.
    """

    chunk_size = int(options.get("chunk_size", 180))
    overlap = int(options.get("overlap", 40))
    source = TOY_PAPERS[0]
    text = f"{source['title']}. {source['text']}"
    chunks = make_chunks(text, chunk_size=chunk_size, overlap=overlap)
    enriched = [
        {
            "chunk_id": f"{source['doc_id']}_c{chunk['chunk_index']:03d}",
            **chunk,
            "metadata": {
                "doi": source["doi"],
                "page": source["page"],
                "section": source["section"],
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
