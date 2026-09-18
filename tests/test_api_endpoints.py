"""Tests for FastAPI HTTP endpoints using TestClient."""

from fastapi.testclient import TestClient

from darukaa.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["corpus_size"] > 0


def test_chat_incomplete_turn_triggers_clarification():
    payload = {
        "message": "Biodiversity is declining on my land",
        "session_id": "api-test-incomplete",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_clarification"] is True
    assert "soil organic carbon %" in data["reply"]
    assert len(data["suggested_quick_replies"]) > 0


def test_chat_complete_benchmark_turn():
    payload = {
        "message": "Soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid",
        "session_id": "api-test-benchmark",
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_clarification"] is False
    assert len(data["recommendations"]) >= 2
    assert any("Agroforestry" in r["title"] for r in data["recommendations"])


def test_analyze_structured_endpoint():
    payload = {
        "soil_organic_carbon_pct": 0.3,
        "rainfall_category": "low",
        "crop": "monoculture wheat",
        "region": "semi-arid",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["active_variables_count"] >= 3
    assert len(data["recommendations"]) >= 2


def test_knowledge_query_endpoint():
    payload = {
        "query": "soil water capacity fao recarbonizing",
        "top_k": 3,
    }
    response = client.post("/api/knowledge/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_matched"] > 0
    assert len(data["results"]) > 0


def test_metrics_correlations_endpoint():
    response = client.get("/api/metrics/correlations")
    assert response.status_code == 200
    data = response.json()
    assert data["total_edges"] >= 7


def test_validation_error_envelope():
    """Validates unified error envelope format for invalid payloads."""
    payload = {
        "query": "",  # min_length=2 violation
    }
    response = client.post("/api/knowledge/query", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data or "code" in data
    # Check that it adheres to standard error envelope
    if "error" in data:
        assert data["error"]["code"] == "VALIDATION_FAILED"
    else:
        assert data["code"] == "VALIDATION_FAILED"
