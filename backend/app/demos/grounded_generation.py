from backend.app.demos.hybrid_retrieval import reciprocal_rank_fusion
from backend.app.demos.sample_data import paper_chunks
from backend.app.demos.utils import GeminiService, format_citation, keyword_score, safe_gemini_call
from backend.app.schemas import DemoResponse, DemoStep


def select_evidence(question: str, top_k: int) -> list[dict]:
    scored = sorted(
        [
            {
                **chunk,
                "retrieval_score": round(keyword_score(question, chunk["content"]), 4),
            }
            for chunk in paper_chunks()
        ],
        key=lambda item: item["retrieval_score"],
        reverse=True,
    )
    if all(item["retrieval_score"] == 0 for item in scored):
        fusion = reciprocal_rank_fusion([[chunk["chunk_id"] for chunk in scored]])
        scored = sorted(scored, key=lambda item: fusion[item["chunk_id"]], reverse=True)
    return scored[:top_k]


def build_prompt(question: str, evidence: list[dict]) -> str:
    evidence_block = "\n\n".join(
        (
            f"[{index}] {chunk['metadata']['title']} "
            f"(DOI: {chunk['metadata']['doi']}, p. {chunk['metadata']['page']}, "
            f"{chunk['metadata']['section']}): {chunk['content']}"
        )
        for index, chunk in enumerate(evidence, start=1)
    )
    return f"""
You are a RAG assistant for a learning demo.
Answer only from the evidence below.
If evidence is insufficient, say what is uncertain.
Use this exact structure:

Direct Answer
Evidence
Limitations
Sources Used

Question:
{question}

Evidence:
{evidence_block}
""".strip()


def extractive_fallback(question: str, evidence: list[dict]) -> str:
    lines = [
        "Direct Answer",
        "The evidence describes ultrasound thermometry, spectral CT, MRI thermometry, and thermocouples as monitoring approaches during thermal ablation.",
        "",
        "Evidence",
    ]
    for index, chunk in enumerate(evidence, start=1):
        lines.append(f"[{index}] {chunk['content']}")
    lines.extend(
        [
            "",
            "Limitations",
            "This fallback answer is extractive because Gemini generation was not available.",
            "",
            "Sources Used",
        ]
    )
    for index, chunk in enumerate(evidence, start=1):
        lines.append(f"[{index}] {chunk['metadata']['title']}, DOI {chunk['metadata']['doi']}")
    return "\n".join(lines)


def run(question: str, options: dict) -> DemoResponse:
    top_k = int(options.get("top_k", 3))
    evidence = select_evidence(question, top_k)
    prompt = build_prompt(question, evidence)
    service = GeminiService()
    generated, gemini_status = safe_gemini_call(
        lambda: service.generate_text(prompt),
        fallback={"provider": "extractive_fallback", "model": None, "text": extractive_fallback(question, evidence)},
    )

    return DemoResponse(
        demo_id="grounded_generation",
        title="07 Grounded Generation",
        concept=(
            "Grounded generation passes retrieved evidence into the prompt and constrains "
            "the LLM to answer with citations."
        ),
        steps=[
            DemoStep(name="selected_evidence", output=evidence),
            DemoStep(name="prompt_sent_to_gemini", output=prompt),
            DemoStep(name="generation_status", output=gemini_status),
        ],
        final_output={
            "answer": generated["text"],
            "provider": generated["provider"],
            "model": generated["model"],
            "sources": [format_citation(chunk, index) for index, chunk in enumerate(evidence, start=1)],
        },
        interview_notes=[
            "RAG does not let the model answer from memory first; it gives evidence first.",
            "The prompt format separates direct answer, evidence, limitations, and sources.",
        ],
    )

