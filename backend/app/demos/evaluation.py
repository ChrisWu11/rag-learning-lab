from backend.app.demos.grounded_generation import select_evidence
from backend.app.demos.sample_data import EVALUATION_SET
from backend.app.schemas import DemoResponse, DemoStep


def reciprocal_rank(results: list[str], relevant_ids: list[str]) -> float:
    """Return 1/rank for the first retrieved relevant chunk.

    Args:
        results: Retrieved chunk IDs ordered from best to worst.
        relevant_ids: Ground-truth chunk IDs that should answer the question.
    """

    for rank, chunk_id in enumerate(results, start=1):
        if chunk_id in relevant_ids:
            return 1 / rank
    return 0.0


def run(question: str, options: dict) -> DemoResponse:
    """Run the RAG evaluation demo.

    Args:
        question: Included for API consistency; evaluation uses its own labelled cases.
        options: Supports top_k, which changes the retrieval cutoff used by metrics.
    """

    top_k = int(options.get("top_k", 3))
    rows = []
    for case in EVALUATION_SET:
        evidence = select_evidence(case["question"], top_k)
        retrieved_ids = [chunk["chunk_id"] for chunk in evidence]
        relevant = set(case["relevant_chunk_ids"])
        retrieved = set(retrieved_ids)
        rows.append(
            {
                "question": case["question"],
                "expected_relevant_chunks": case["relevant_chunk_ids"],
                "retrieved_chunks": retrieved_ids,
                "retrieval_hit": bool(relevant & retrieved),
                "reciprocal_rank": round(reciprocal_rank(retrieved_ids, case["relevant_chunk_ids"]), 3),
                "generation_claim_check": {
                    "required_claims": case["required_claims"],
                    "note": "In a full evaluation, these claims would be checked against the generated answer.",
                },
                "citation_support_check": "Verify that every cited chunk actually supports the sentence using it.",
            }
        )
    hit_rate = sum(1 for row in rows if row["retrieval_hit"]) / len(rows)
    mrr = sum(row["reciprocal_rank"] for row in rows) / len(rows)

    return DemoResponse(
        demo_id="evaluation",
        title="09 Evaluation",
        concept=(
            "RAG should be evaluated by components: retrieval, reranking, generation "
            "faithfulness, and citation support."
        ),
        steps=[
            DemoStep(name="labelled_qa_set", output=EVALUATION_SET),
            DemoStep(name="per_question_results", output=rows),
        ],
        final_output={
            "retrieval_hit_rate": round(hit_rate, 3),
            "mean_reciprocal_rank": round(mrr, 3),
            "generation_metric": "faithfulness against retrieved evidence",
            "citation_metric": "whether each citation supports the specific claim",
        },
        interview_notes=[
            "A final answer can look correct even when retrieval is wrong, so I evaluate components separately.",
            "Retrieval metrics tell whether the system found evidence before judging answer wording.",
        ],
    )
