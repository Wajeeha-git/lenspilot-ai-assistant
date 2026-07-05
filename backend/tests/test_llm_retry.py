"""
Tests for call_llm()'s retry-on-429 behavior and status code propagation.
Uses a real requests.Response (with a fake body) to build a realistic
google.genai.errors.APIError without needing a live Gemini call.
"""
import json
from unittest.mock import MagicMock, patch

import pytest
import requests
from google.genai import errors

from app.services.llm import call_llm, LLMError


def _fake_api_error(code: int, message: str = "error") -> errors.APIError:
    response = requests.Response()
    response.status_code = code
    response._content = json.dumps({"message": message, "status": "ERROR"}).encode()
    return errors.APIError(code, response)


MESSAGES = [
    {"role": "system", "content": "You are a test assistant."},
    {"role": "user", "content": "hello"},
]


@patch("app.services.llm._get_client")
@patch("app.services.llm.time.sleep", return_value=None)  # skip real backoff delays in tests
def test_call_llm_retries_429_then_succeeds(mock_sleep, mock_get_client):
    mock_client = MagicMock()
    fake_response = MagicMock()
    fake_response.text = "a real answer"

    # First call raises 429, second call succeeds
    mock_client.models.generate_content.side_effect = [
        _fake_api_error(429, "rate limited"),
        fake_response,
    ]
    mock_get_client.return_value = mock_client

    result = call_llm(MESSAGES, max_retries=3)

    assert result == "a real answer"
    assert mock_client.models.generate_content.call_count == 2
    mock_sleep.assert_called_once()  # backed off exactly once before

@patch("app.services.llm._get_client")
@patch("app.services.llm.time.sleep", return_value=None)
def test_call_llm_raises_429_after_retries_exhausted(mock_sleep, mock_get_client):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = _fake_api_error(429, "still limited")
    mock_get_client.return_value = mock_client

    with pytest.raises(LLMError) as exc_info:
        call_llm(MESSAGES, max_retries=2)

    assert exc_info.value.status_code == 429
    assert mock_client.models.generate_content.call_count == 3

@patch("app.services.llm._get_client")
def test_call_llm_auth_error_maps_to_502_no_retry(mock_get_client):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = _fake_api_error(401, "bad key")
    mock_get_client.return_value = mock_client

    with pytest.raises(LLMError) as exc_info:
        call_llm(MESSAGES)

    assert exc_info.value.status_code == 502
    assert mock_client.models.generate_content.call_count == 1

@patch("app.services.llm._get_client")
def test_call_llm_timeout_maps_to_504(mock_get_client):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = _fake_api_error(504, "timed out")
    mock_get_client.return_value = mock_client

    with pytest.raises(LLMError) as exc_info:
        call_llm(MESSAGES)

    assert exc_info.value.status_code == 504
