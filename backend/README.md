# LensPilot Brain API

FastAPI RAG backend for the LensPilot AI Assistant. It receives questions
from the chatbot widget, retrieves relevant LensPilot document chunks from
Postgres/pgvector, calls the configured LLM, and returns an answer with
sources.

## What Is Included

- FastAPI app with `/health`, `/chat`, and `/ingest`
- Versioned aliases under `/api/v1`
- PostgreSQL schema managed by Alembic
- pgvector-backed document chunk search
- File ingestion pipeline for `.md`, `.txt`, `.html`, and `.pdf`
- Placeholder LensPilot docs for local testing
- GitHub CI support for tests and migrations

## Local Setup

See [docs/BACKEND_SETUP.md](docs/BACKEND_SETUP.md).

## API Contract

The shared frontend/backend contract lives at [../docs/API.md](../docs/API.md).
Backend-local notes are in [docs/API.md](docs/API.md).

Security notes live at [../docs/SECURITY.md](../docs/SECURITY.md).

## Placeholder Content

These two pieces are intentionally temporary until the Knowledge/Prompt owner
replaces them with official LensPilot material:

- `ingestion/knowledge_base/` - real LensPilot knowledge base (12 topic docs with frontmatter metadata)
- `app/services/prompt.py` - composes the real system prompt from `prompt_sources/` (see that folder's README note)

Swapping either later does not require API or database schema changes.
