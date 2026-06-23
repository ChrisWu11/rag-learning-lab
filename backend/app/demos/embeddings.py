from backend.app.demos.sample_data import paper_chunks
from backend.app.demos.utils import GeminiService, cosine_similarity, fallback_embedding, safe_gemini_call
from backend.app.schemas import DemoResponse, DemoStep


def run(question: str, options: dict) -> DemoResponse:
    chunks = paper_chunks()
    texts = [question] + [chunk["content"] for chunk in chunks]
    service = GeminiService()
    vectors, gemini_status = safe_gemini_call(
        lambda: service.embed_texts(texts),
        fallback=([fallback_embedding(text) for text in texts], {"provider": "local_fallback", "dimensions": 32}),
    )
    embeddings, model_info = vectors
    query_vector = embeddings[0]
    chunk_vectors = embeddings[1:]
    scored = []
    for chunk, vector in zip(chunks, chunk_vectors, strict=True):
        scored.append(
            {
                "chunk_id": chunk["chunk_id"],
                "title": chunk["metadata"]["title"],
                "score": round(cosine_similarity(query_vector, vector), 4),
                "content": chunk["content"],
            }
        )
    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)
    top_k = int(options.get("top_k", 3))

    return DemoResponse(
        demo_id="embeddings",
        title="04 Embedding & Vector Search",
        concept=(
            "Embedding search converts the query and chunks into vectors, then retrieves "
            "the chunks with the highest cosine similarity."
        ),
        steps=[
            DemoStep(name="query", output=question),
            DemoStep(name="embedding_model", output={**model_info, "gemini_status": gemini_status}),
            DemoStep(
                name="vector_preview",
                output={
                    "query_vector_first_8_values": [round(value, 4) for value in query_vector[:8]],
                    "full_dimension": len(query_vector),
                },
            ),
            DemoStep(name="ranked_by_cosine_similarity", output=ranked),
        ],
        final_output={"top_k": top_k, "results": ranked[:top_k]},
        interview_notes=[
            "Vector retrieval handles semantic similarity even when exact keywords differ.",
            "I do not show the full vector in the UI because the concept is similarity, not raw numbers.",
        ],
    )

