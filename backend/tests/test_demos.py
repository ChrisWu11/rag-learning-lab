from fastapi.testclient import TestClient

from backend.app.config import get_settings
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


def test_chunking_preserves_metadata() -> None:
    response = client.post(
        "/api/demos/chunking/run",
        json={"question": "test", "options": {"chunk_size": 120, "overlap": 20}},
    )
    assert response.status_code == 200
    chunks = response.json()["steps"][2]["output"]
    assert chunks[0]["metadata"]["doi"]
    assert chunks[0]["metadata"]["page"]


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
