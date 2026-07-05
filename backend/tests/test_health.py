"""
Minimal smoke test that doesn't require a live DB or Gemini key.
Run with: pytest
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_versioned_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422  # pydantic validation error


def test_versioned_chat_rejects_empty_message():
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422  # pydantic validation error
