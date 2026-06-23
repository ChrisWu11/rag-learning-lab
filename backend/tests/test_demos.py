from fastapi.testclient import TestClient

from backend.app.config import get_settings
from backend.app.demos.pdf_document import SAMPLE_PDF_PATH, parse_sample_pdf
from backend.app.main import app

client = TestClient(app)


def setup_function() -> None:
    get_settings.cache_clear()


def teardown_function() -> None:
    get_settings.cache_clear()


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def find_step(payload: dict, name: str) -> dict:
    return next(step for step in payload["steps"] if step["name"] == name)


def test_sample_pdf_exists_and_has_extractable_metadata() -> None:
    assert SAMPLE_PDF_PATH.exists()
    parsed = parse_sample_pdf()
    assert parsed["pdf_info"]["page_count"] >= 2
    assert parsed["document_metadata"]["title"] == "Tiny Ultrasound Thermometry Demo Paper"
    assert parsed["document_metadata"]["doi"] == "10.0000/rag-learning-lab.2026.001"
    assert parsed["document_metadata"]["year"] == 2026


def test_pdf_parsing_demo_uses_real_pdf() -> None:
    response = client.post(
        "/api/demos/pdf_parsing/run",
        json={"question": "unused", "options": {}},
    )
    assert response.status_code == 200
    payload = response.json()
    file_info = find_step(payload, "pdf_file_info")["output"]
    records = find_step(payload, "cleaned_page_records")["output"]
    assert file_info["file_name"] == "tiny_ablation_paper.pdf"
    assert file_info["exists"] is True
    assert len(records) >= 2
    assert records[0]["section"] == "Abstract"


def test_corpus_metadata_demo_uses_pdf_metadata() -> None:
    response = client.post(
        "/api/demos/corpus_metadata/run",
        json={"question": "unused", "options": {}},
    )
    assert response.status_code == 200
    payload = response.json()
    metadata = find_step(payload, "extracted_document_metadata")["output"]
    citation_cards = find_step(payload, "citation_cards")["output"]
    assert metadata["source_type"] == "pdf"
    assert metadata["doi"] == "10.0000/rag-learning-lab.2026.001"
    assert citation_cards[0]["source_type"] == "pdf"


def test_chunking_preserves_metadata() -> None:
    response = client.post(
        "/api/demos/chunking/run",
        json={"question": "test", "options": {"chunk_size": 120, "overlap": 20}},
    )
    assert response.status_code == 200
    chunks = find_step(response.json(), "chunks_with_metadata")["output"]
    assert chunks[0]["metadata"]["doi"]
    assert chunks[0]["metadata"]["source_path"].endswith("tiny_ablation_paper.pdf")
    assert chunks[0]["metadata"]["pages"]
    assert chunks[0]["metadata"]["sections"]


def test_embedding_search_returns_top_k_with_fallback_without_key(monkeypatch) -> None:
    monkeypatch.setenv("DISABLE_GEMINI", "true")
    get_settings.cache_clear()
    response = client.post(
        "/api/demos/embeddings/run",
        json={"question": "MRI thermometry temperature map", "options": {"top_k": 2}},
    )
    assert response.status_code == 200
    assert len(response.json()["final_output"]["results"]) == 2


def test_hybrid_retrieval_returns_fused_results(monkeypatch) -> None:
    monkeypatch.setenv("DISABLE_GEMINI", "true")
    get_settings.cache_clear()
    response = client.post(
        "/api/demos/hybrid_retrieval/run",
        json={"question": "ultrasound speed of sound thermometry", "options": {"top_k": 3}},
    )
    assert response.status_code == 200
    step_names = [step["name"] for step in response.json()["steps"]]
    assert "hybrid_rrf_results" in step_names


def test_generation_prompt_contains_evidence(monkeypatch) -> None:
    monkeypatch.setenv("DISABLE_GEMINI", "true")
    get_settings.cache_clear()
    response = client.post(
        "/api/demos/grounded_generation/run",
        json={"question": "What can monitor temperature?", "options": {"top_k": 2}},
    )
    assert response.status_code == 200
    prompt = response.json()["steps"][1]["output"]
    assert "Evidence:" in prompt
    assert response.json()["final_output"]["sources"]


def test_evaluation_metrics_exist() -> None:
    response = client.post(
        "/api/demos/evaluation/run",
        json={"question": "unused", "options": {"top_k": 3}},
    )
    assert response.status_code == 200
    final_output = response.json()["final_output"]
    assert "retrieval_hit_rate" in final_output
    assert "mean_reciprocal_rank" in final_output
