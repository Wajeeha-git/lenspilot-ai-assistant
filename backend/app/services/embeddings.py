"""
Wraps the embedding model so the rest of the app never talks to OpenAI directly.
Swap this file out if you switch embedding providers later.
"""
from openai import OpenAI

from app.core.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your .env file before calling the embedding API."
            )
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def embed_text(text: str) -> list[float]:
    """Embed a single string. Used for embedding the user's live question."""
    return embed_texts([text])[0]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of strings in one API call. Used during ingestion."""
    client = _get_client()
    response = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=texts)
    # response.data is returned in the same order as the input list
    return [item.embedding for item in response.data]
