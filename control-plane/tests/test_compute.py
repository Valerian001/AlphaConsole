import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.vast_svc import vast_orchestrator

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "AlphaConsole Control Plane"

def test_get_offers_fail_no_api_key(monkeypatch):
    # Mock empty offers
    monkeypatch.setattr(vast_orchestrator, "filter_instances", lambda: [])
    response = client.get("/compute/offers")
    assert response.status_code == 503
    assert response.json()["detail"] == "No matching Vast.ai offers found."

def test_get_offers_success(monkeypatch):
    # Mock successful offers
    mock_offers = [{"id": 1, "dph_total": 0.5, "gpu_name": "RTX 4090"}]
    monkeypatch.setattr(vast_orchestrator, "filter_instances", lambda: mock_offers)
    
    response = client.get("/compute/offers")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["gpu_name"] == "RTX 4090"
