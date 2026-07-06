# LensPilot Backend

FastAPI backend for the LensPilot AI Assistant. It receives widget questions,
retrieves relevant LensPilot document chunks from PostgreSQL/pgvector, builds a
grounded prompt, calls Gemini when needed, and returns an answer with sources.

## Included

- FastAPI app with `/health`, `/chat`, and `/ingest`
- Versioned API routes under `/api/v1`
- PostgreSQL schema managed by Alembic
- pgvector-backed document retrieval
- Markdown/HTML/TXT/PDF ingestion pipeline
- LensPilot knowledge-base documents with metadata
- Prompt source files for identity, tone, and refusal rules
- Deterministic local fallback for approved FAQ/demo/refusal questions
- Tests for health, security, retry behavior, ingestion, and local assistant logic

## Local Setup

See [docs/BACKEND_SETUP.md](docs/BACKEND_SETUP.md).

## API Contract

The shared frontend/backend contract lives at [../docs/API.md](../docs/API.md).
Backend-local notes are in [docs/API.md](docs/API.md).

Security notes live at [../docs/SECURITY.md](../docs/SECURITY.md).

## Runtime Flow

1. The widget posts a message to `/api/v1/chat`.
2. The backend creates or reuses a chat session.
3. Known LensPilot FAQ/workflow/refusal cases are answered locally.
4. For other in-scope questions, retrieval finds relevant public document chunks.
5. Prompt rules and retrieved context are sent to Gemini.
6. The answer and sources are returned to the widget.
