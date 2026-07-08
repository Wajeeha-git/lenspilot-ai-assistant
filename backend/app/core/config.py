"""
Central place for all environment/config values.
Everything is read from environment variables (loaded from .env in dev).
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- App ---
    APP_NAME: str = "LensPilot Brain API"
    ENV: str = os.getenv("ENV", "development")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    API_KEY: str | None = os.getenv("API_KEY")  # optional simple auth for /chat, /ingest

    # --- CORS ---
    # Comma separated list of allowed origins, e.g. "https://lenspilot.com,http://localhost:3000"
    CORS_ORIGINS: list[str] = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()
    ]

    # --- Database ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/lenspilot_ai",
    )

    # --- Gemini (Google AI) ---
    # Chosen for the demo: genuine free tier, no card required, works for
    # both embeddings and chat. See app/services/embeddings.py and llm.py
    # for provider-specific notes (esp. the 1-text-per-request limit on
    # embeddings, and free-tier rate limits).
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
    # gemini-embedding-001 defaults to 3072 dims, but supports output_dimensionality
    # to shrink it -- kept at 1536 to match the existing pgvector column and
    # avoid a migration when switching providers.
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "1536"))
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gemini-2.5-flash")

    # --- RAG tuning ---
    CHUNK_SIZE_WORDS: int = int(os.getenv("CHUNK_SIZE_WORDS", "350"))
    CHUNK_OVERLAP_WORDS: int = int(os.getenv("CHUNK_OVERLAP_WORDS", "30"))
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", "5"))

    # --- Ingestion ---
    INGESTION_DOCS_DIR: str = os.getenv(
        "INGESTION_DOCS_DIR",
        os.path.join(os.path.dirname(__file__), "..", "..", "ingestion", "knowledge_base"),
    )

    # --- Security / rate limiting ---
    # Max requests per client per rolling 60s window. Set to 0 to disable.
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()


def validate_settings_or_warn():
    """
    Fail loudly in production, but only warn in development, when settings are
    convenient for local work but risky for a public deployment.
    """
    import logging

    logger = logging.getLogger("lenspilot")
    is_prod = settings.ENV.lower() in ("production", "prod")

    problems = []
    if settings.CORS_ORIGINS == ["*"]:
        problems.append("CORS_ORIGINS is '*'")
    if is_prod and "postgres:postgres@localhost" in settings.DATABASE_URL:
        problems.append("DATABASE_URL still looks like the local default")

    # API_KEY is optional in production to allow public chat widgets to function.
    # Print a warning instead of raising a fatal exception.
    if not settings.API_KEY:
        logger.warning("[security warning] API_KEY is not set. Anyone can query the API endpoints.")

    if problems and is_prod:
        raise RuntimeError(
            "Refusing to start with ENV=production and insecure settings: "
            + "; ".join(problems)
        )

    for problem in problems:
        logger.warning("[dev-only config warning] %s", problem)
