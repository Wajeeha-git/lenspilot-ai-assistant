"""
Security and error-handling checks that do not require a live DB or OpenAI key.
"""
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings, validate_settings_or_warn
from app.core.middleware import _hits
from app.main import app

client = TestClient(app)


def test_validation_error_uses_error_envelope():
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422
    assert "error" in response.json()
    assert "detail" not in response.json()


def test_http_error_uses_error_envelope():
    response = client.get("/missing-route")

    assert response.status_code == 404
    assert response.json() == {"error": "Not Found"}


def test_auth_error_uses_error_envelope(monkeypatch):
    monkeypatch.setattr(settings, "API_KEY", "secret")
    _hits.clear()

    response = client.post("/chat", json={"message": "hello"})

    assert response.status_code == 401
    assert response.json() == {"error": "Invalid or missing API key"}


def test_response_has_request_id_header():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["x-request-id"]


def test_api_v1_alias_matches_root():
    root = client.get("/health")
    versioned = client.get("/api/v1/health")

    assert root.status_code == versioned.status_code == 200
    assert root.json() == versioned.json()


def test_rate_limit_returns_429_with_error_envelope(monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 3)
    _hits.clear()

    responses = [
        client.post("/chat", json={"message": ""}, headers={"x-api-key": "test-key"})
        for _ in range(4)
    ]

    assert [response.status_code for response in responses] == [422, 422, 422, 429]
    assert responses[-1].json()["error"].startswith("Too many requests")
    assert responses[-1].headers["x-request-id"]


def test_bearer_token_is_used_as_rate_limit_key(monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 1)
    _hits.clear()

    headers = {"Authorization": "Bearer bearer-test-key"}
    first = client.post("/api/v1/chat", json={"message": ""}, headers=headers)
    second = client.post("/api/v1/chat", json={"message": ""}, headers=headers)

    assert first.status_code == 422
    assert second.status_code == 429


def test_rate_limit_disabled_when_zero(monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MINUTE", 0)
    _hits.clear()

    responses = [client.post("/chat", json={"message": ""}) for _ in range(5)]

    assert all(response.status_code == 422 for response in responses)


def test_production_validation_fails_fast(monkeypatch):
    monkeypatch.setattr(settings, "ENV", "production")
    monkeypatch.setattr(settings, "CORS_ORIGINS", ["*"])
    monkeypatch.setattr(settings, "API_KEY", None)

    with pytest.raises(RuntimeError):
        validate_settings_or_warn()
