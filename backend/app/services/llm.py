"""
Wraps the chat/completion model. Swap this file out if you switch LLM providers.

call_llm() keeps accepting the same `messages` shape that build_messages()
in prompt.py already produces ([{"role": "system", ...}, {"role": "user",
...}]) so nothing in routes.py or prompt.py needed to change for this
provider swap -- this function just translates that shape into Gemini's
system_instruction + contents split internally.

Retry note: Gemini's free tier is limited to ~10 requests/minute for
gemini-2.5-flash. A single /chat call already makes one embedding request
(embeddings.py) plus one chat request (here) -- a burst of several chat
messages in under a minute can exceed that easily. This retries a 429 a
few times with backoff before giving up, matching the same pattern
embeddings.py already uses for embedding calls.
"""
import logging
import time

from google import genai
from google.genai import types
from google.genai import errors

from app.core.config import settings

logger = logging.getLogger("lenspilot")

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to your .env file before calling the chat API."
            )
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


class LLMError(Exception):
    """
    Raised when the LLM call fails in a way the caller should handle gracefully.
    `status_code` lets routes.py return the right HTTP status instead of a
    flat 502 for every failure mode (e.g. 429 for rate limits, 504 for
    timeouts).
    """

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def call_llm(messages: list[dict], max_retries: int = 3) -> str:
    """
    Send messages to the chat model and return the reply text.
    Raises LLMError on any failure so the API layer can return a clean error response.
    Retries with backoff on 429 (rate limit) before giving up.
    """
    client = _get_client()

    system_instruction = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    user_content = "\n\n".join(m["content"] for m in messages if m["role"] != "system")

    delay = 2.0
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=settings.CHAT_MODEL,
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction or None,
                    temperature=0.2,
                ),
            )
            if not response.text:
                raise LLMError("The AI provider returned an empty response.", status_code=502)
            return response.text.strip()
        except errors.APIError as e:
            code = getattr(e, "code", None)

            if code == 429 and attempt < max_retries:
                logger.warning("LLM rate-limited (attempt %d), retrying in %.0fs", attempt + 1, delay)
                time.sleep(delay)
                delay *= 2
                continue

            if code in (401, 403):
                logger.error("LLM auth error: %s", e)
                raise LLMError(
                    "The AI provider rejected our API key. Check GEMINI_API_KEY.", status_code=502
                ) from e
            if code == 429:
                logger.error("LLM rate limit (retries exhausted): %s", e)
                raise LLMError(
                    "The AI provider is rate-limiting us. Please try again shortly.", status_code=429
                ) from e
            if code == 504:
                logger.error("LLM timeout: %s", e)
                raise LLMError("The AI provider timed out. Please try again.", status_code=504) from e
            logger.error("LLM API error: %s", e)
            raise LLMError("The AI provider returned an error.", status_code=502) from e
