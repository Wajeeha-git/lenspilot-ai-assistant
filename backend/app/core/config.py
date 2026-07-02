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

    # --- OpenAI ---
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "1536"))
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")

    # --- RAG tuning ---
    CHUNK_SIZE_WORDS: int = int(os.getenv("CHUNK_SIZE_WORDS", "350"))
    CHUNK_OVERLAP_WORDS: int = int(os.getenv("CHUNK_OVERLAP_WORDS", "50"))
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", "5"))

    # --- Ingestion ---
    INGESTION_DOCS_DIR: str = os.getenv(
        "INGESTION_DOCS_DIR",
        os.path.join(os.path.dirname(__file__), "..", "..", "ingestion", "sample_docs"),
    )


settings = Settings()
