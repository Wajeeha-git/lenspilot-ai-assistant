"""
Wraps the embedding model so the rest of the app never talks to Gemini
directly. Swap this file out if you switch embedding providers later.

Provider notes (Gemini / gemini-embedding-001):
- Unlike OpenAI's embeddings endpoint, Gemini only accepts ONE text per
  request (no batch input) as of this model's current API. embed_texts()
  therefore loops -- fine for this project's small corpus (~80 chunks),
  but worth knowing if the knowledge base grows much larger.
- Uses task_type to distinguish indexing (embed_texts, called only during
  ingestion) from querying (embed_text, called only for the live user
  question in retrieval.py) -- this is Gemini's recommended way to get
  better asymmetric retrieval quality, not just a formality.
- output_dimensionality=1536 keeps vectors compatible with the existing
  pgvector column (the model defaults to 3072-dim otherwise), so switching
  providers didn't require a schema migration.
- Free tier rate limits are real and can be low; embed_texts() retries a
  few times with backoff on 429s so a normal ingestion run doesn't fail
  outright on a transient rate limit.
"""
import time
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
                "GEMINI_API_KEY is not set. Add it to your .env file before calling the embedding API."
            )
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _embed_one(text: str, task_type: str, max_retries: int = 3) -> list[float]:
    client = _get_client()
    delay = 2.0
    for attempt in range(max_retries + 1):
        try:
            response = client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=settings.EMBEDDING_DIM,
                ),
            )
            return response.embeddings[0].values
        except errors.APIError as e:
            if e.code == 429 and attempt < max_retries:
                logger.warning("Embedding rate-limited (attempt %d), retrying in %.0fs", attempt + 1, delay)
                time.sleep(delay)
                delay *= 2
                continue
            raise


def embed_text(text: str) -> list[float]:
    """Embed a single user question for retrieval-time similarity search."""
    return _embed_one(text, task_type="RETRIEVAL_QUERY")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of document chunks during ingestion (one request per text)."""
    return [_embed_one(text, task_type="RETRIEVAL_DOCUMENT") for text in texts]
