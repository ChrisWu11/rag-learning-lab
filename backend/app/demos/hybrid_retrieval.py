from backend.app.demos.sample_data import paper_chunks
from backend.app.demos.utils import (
    GeminiService,
    cosine_similarity,
    fallback_embedding,
    keyword_score,
    safe_gemini_call,
)
from backend.app.schemas import DemoResponse, DemoStep


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fuse multiple ranked lists without requiring comparable raw scores.

    Args:
        rankings: Each inner list contains chunk IDs ordered from best to worst.
        k: Smoothing constant. Larger values reduce the impact of top ranks.
    """

    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank)
    return scores


def run(question: str, options: dict) -> DemoResponse:
    """Run the hybrid retrieval demo.

    Args:
        question: User query used for both vector search and keyword scoring.
        options: Supports top_k, the number of fused results shown in final_output.
    """

    chunks = paper_chunks()
    service = GeminiService()
    texts = [question] + [chunk["content"] for chunk in chunks]
    vectors, gemini_status = safe_gemini_call(
        lambda: service.embed_texts(texts),
        fallback=([fallback_embedding(text) for text in texts], {"provider": "local_fallback", "dimensions": 32}),
    )
    embeddings, model_info = vectors
    query_vector = embeddings[0]

    vector_results = []
    keyword_results = []
    for chunk, vector in zip(chunks, embeddings[1:], strict=True):
        vector_results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "title": chunk["metadata"]["title"],
                "score": round(cosine_similarity(query_vector, vector), 4),
            }
        )
        keyword_results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "title": chunk["metadata"]["title"],
                "score": round(keyword_score(question, chunk["content"]), 4),
            }
        )

    vector_ranked = sorted(vector_results, key=lambda item: item["score"], reverse=True)
    keyword_ranked = sorted(keyword_results, key=lambda item: item["score"], reverse=True)
    # RRF combines only rank positions, so vector and keyword scores do not need
    # to share the same numeric scale.
    fusion_scores = reciprocal_rank_fusion(
        [[item["chunk_id"] for item in vector_ranked], [item["chunk_id"] for item in keyword_ranked]]
    )
    chunk_lookup = {chunk["chunk_id"]: chunk for chunk in chunks}
    hybrid_ranked = [
        {
            "chunk_id": chunk_id,
            "title": chunk_lookup[chunk_id]["metadata"]["title"],
            "rrf_score": round(score, 5),
            "content": chunk_lookup[chunk_id]["content"],
        }
        for chunk_id, score in sorted(fusion_scores.items(), key=lambda item: item[1], reverse=True)
    ]

    return DemoResponse(
        demo_id="hybrid_retrieval",
        title="05 Hybrid Retrieval",
        concept=(
            "Hybrid retrieval combines semantic vector search with keyword matching. "
            "This is useful in scientific corpora where abbreviations, method names, and DOI-like terms matter."
        ),
        steps=[
            DemoStep(name="embedding_model", output={**model_info, "gemini_status": gemini_status}),
            DemoStep(name="vector_results", output=vector_ranked),
            DemoStep(name="keyword_results", output=keyword_ranked),
            DemoStep(name="hybrid_rrf_results", output=hybrid_ranked),
        ],
        final_output={"top_k": int(options.get("top_k", 3)), "results": hybrid_ranked[: int(options.get("top_k", 3))]},
        interview_notes=[
            "Vector search is strong for semantic meaning; keyword search protects exact scientific terms.",
            "RRF is a simple way to fuse rankings without needing both scores on the same scale.",
        ],
    )
