from backend.app.demos.hybrid_retrieval import reciprocal_rank_fusion
from backend.app.demos.sample_data import paper_chunks
from backend.app.demos.utils import keyword_score, tokenize
from backend.app.schemas import DemoResponse, DemoStep


def explainable_rerank_score(question: str, text: str) -> float:
    base = keyword_score(question, text)
    query_terms = set(tokenize(question))
    text_terms = set(tokenize(text))
    method_bonus = 0.0
    for term in ["ultrasound", "ct", "mri", "thermocouple", "temperature", "ablation"]:
        if term in query_terms and term in text_terms:
            method_bonus += 0.08
    return round(base + method_bonus, 4)


def run(question: str, options: dict) -> DemoResponse:
    chunks = paper_chunks()
    initial_scores = reciprocal_rank_fusion(
        [
            [chunk["chunk_id"] for chunk in chunks],
            [chunk["chunk_id"] for chunk in reversed(chunks)],
        ]
    )
    initial_results = [
        {
            "chunk_id": chunk["chunk_id"],
            "title": chunk["metadata"]["title"],
            "initial_score": round(initial_scores[chunk["chunk_id"]], 5),
            "content": chunk["content"],
        }
        for chunk in chunks
    ]
    reranked = sorted(
        [
            {
                **item,
                "reranker_score": explainable_rerank_score(question, item["content"]),
                "reason": "term overlap plus method-name bonus",
            }
            for item in initial_results
        ],
        key=lambda item: item["reranker_score"],
        reverse=True,
    )

    return DemoResponse(
        demo_id="reranking",
        title="06 Reranking",
        concept=(
            "A retriever finds candidate chunks. A reranker then re-scores each query/chunk "
            "pair to push the most directly useful evidence higher."
        ),
        steps=[
            DemoStep(name="initial_top_k_candidates", output=initial_results),
            DemoStep(name="reranked_candidates", output=reranked),
        ],
        final_output={"results": reranked[: int(options.get("top_k", 3))]},
        interview_notes=[
            "This demo uses an explainable scoring function so the reranking idea is visible.",
            "In the final project, the same boundary can be replaced by a CrossEncoder reranker.",
        ],
    )

