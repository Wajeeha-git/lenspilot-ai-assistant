# Backend Setup Guide

## 1. Prerequisites

- Python 3.11+ recommended
- PostgreSQL 14+ with pgvector, or Docker for the provided pgvector image
- OpenAI API key for live ingestion and chat responses

## 2. Install Dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure Environment

```bash
cp .env.example .env
```

Set at minimum:

- `DATABASE_URL`
- `OPENAI_API_KEY`

Leave `API_KEY` blank for local development, or set it to require either
`x-api-key: <key>` or `Authorization: Bearer <key>` on `/chat` and `/ingest`.

## 4. Start Postgres With pgvector

Easiest local path:

```bash
docker compose up -d postgres
```

Manual local Postgres path:

```bash
createdb lenspilot_ai
psql -d lenspilot_ai -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

The first Alembic migration also runs `CREATE EXTENSION IF NOT EXISTS vector`.

## 5. Run Migrations

```bash
alembic upgrade head
```

Expected tables:

- `documents`
- `chunks`
- `chat_sessions`
- `chat_messages`

## 6. Run Ingestion

```bash
python ingestion/ingest.py
```

This loads the LensPilot knowledge base from `ingestion/knowledge_base/`,
chunks each file by section/heading (so an FAQ answer never gets split
mid-sentence), embeds the chunks, and stores them in Postgres alongside
each document's metadata. Unchanged files are skipped on reruns (content
hash check).

### Knowledge base file format

Each `.md` file may start with a small frontmatter block:

```
---
title: FAQ - Customer
category: FAQ
audience: customer
source: LensPilot Knowledge Base v1
version: 2026-07-03
public: true
---
# body starts here...
```

All fields are optional -- ingestion falls back to a filename-based guess
for `title`/`category`, and to `public`/`true` for `audience`/`public`.
`public: false` hard-excludes a document from `/chat` retrieval regardless
of similarity score (see `docs/SECURITY.md`).

To add or update content: add/edit a file in `ingestion/knowledge_base/`,
then rerun `python ingestion/ingest.py`.

### System prompt / behavior rules

These are **not** ingested as retrievable documents -- see the comment at
the top of `app/services/prompt.py` for why. To change the assistant's
identity, tone, or hard rules, edit the plain-text files directly:
- `app/services/prompt_sources/system_prompt.md`
- `app/services/prompt_sources/tone_and_personality.md`
- `app/services/prompt_sources/do_not_do.md`

No Python changes or re-ingestion needed -- they're read fresh each time
the app starts.

## 7. Run The API

```bash
uvicorn app.main:app --reload
```

## 8. Test The API

```bash
curl http://localhost:8000/api/v1/health

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Does LensPilot have a free trial?"}'
```

Unversioned local compatibility routes also work:

```bash
curl http://localhost:8000/health
```

## 9. Run Tests

```bash
pytest
```

## Notes

- Embeddings and chat completions call the OpenAI API and cost money per token.
- `RETRIEVAL_TOP_K` controls how many chunks are sent to the LLM per question.
- `RATE_LIMIT_PER_MINUTE` controls per-client rate limiting for `/chat` and
  `/ingest`. The default is `30`; set it to `0` only for trusted local testing.
- `ENV=production` refuses to boot with unsafe public settings such as
  `CORS_ORIGINS=*` or a missing `API_KEY`.
- Docker was not available in the current local environment during setup, so
  live pgvector migration verification should run in GitHub CI or on a machine
  with Docker/Postgres installed.
