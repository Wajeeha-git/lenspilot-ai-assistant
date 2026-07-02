"""
Wraps the chat/completion model. Swap this file out if you switch LLM providers.
"""
import logging

from openai import OpenAI, APIError, APITimeoutError, RateLimitError, AuthenticationError

from app.core.config import settings

logger = logging.getLogger("lenspilot")

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your .env file before calling the chat API."
            )
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


class LLMError(Exception):
    """Raised when the LLM call fails in a way the caller should handle gracefully."""


def call_llm(messages: list[dict]) -> str:
    """
    Send messages to the chat model and return the reply text.
    Raises LLMError on any failure so the API layer can return a clean error response.
    """
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=messages,
            temperature=0.2,
            timeout=30,
        )
        return response.choices[0].message.content.strip()
    except AuthenticationError as e:
        logger.error("LLM auth error: %s", e)
        raise LLMError("The AI provider rejected our API key. Check OPENAI_API_KEY.") from e
    except RateLimitError as e:
        logger.error("LLM rate limit: %s", e)
        raise LLMError("The AI provider is rate-limiting us. Please try again shortly.") from e
    except APITimeoutError as e:
        logger.error("LLM timeout: %s", e)
        raise LLMError("The AI provider timed out. Please try again.") from e
    except APIError as e:
        logger.error("LLM API error: %s", e)
        raise LLMError("The AI provider returned an error.") from e
