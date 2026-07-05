"""
Wraps the chat/completion model. Swap this file out if you switch LLM providers.

call_llm() keeps accepting the same `messages` shape that build_messages()
in prompt.py already produces ([{"role": "system", ...}, {"role": "user",
...}]) so nothing in routes.py or prompt.py needed to change for this
provider swap -- this function just translates that shape into Gemini's
system_instruction + contents split internally.
"""
import logging

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
    """Raised when the LLM call fails in a way the caller should handle gracefully."""


def call_llm(messages: list[dict]) -> str:
    """
    Send messages to the chat model and return the reply text.
    Raises LLMError on any failure so the API layer can return a clean error response.
    """
    client = _get_client()

    system_instruction = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    user_content = "\n\n".join(m["content"] for m in messages if m["role"] != "system")

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
            raise LLMError("The AI provider returned an empty response.")
        return response.text.strip()
    except errors.APIError as e:
        code = getattr(e, "code", None)
        if code in (401, 403):
            logger.error("LLM auth error: %s", e)
            raise LLMError("The AI provider rejected our API key. Check GEMINI_API_KEY.") from e
        if code == 429:
            logger.error("LLM rate limit: %s", e)
            raise LLMError("The AI provider is rate-limiting us. Please try again shortly.") from e
        if code == 504:
            logger.error("LLM timeout: %s", e)
            raise LLMError("The AI provider timed out. Please try again.") from e
        logger.error("LLM API error: %s", e)
        raise LLMError("The AI provider returned an error.") from e
