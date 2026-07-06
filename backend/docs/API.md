# LensPilot Brain API Contract

Base URL for integrations:

```text
http://localhost:8000/api/v1
```

For local smoke tests, the same endpoints are also exposed without the
`/api/v1` prefix.

All responses are JSON. Error responses use `{"error": "..."}`.

If `API_KEY` is set, `/chat` and `/ingest` require either:

```text
x-api-key: <API_KEY>
Authorization: Bearer <API_KEY>
```

## GET /health

Response `200 OK`:

```json
{
  "status": "ok"
}
```

## POST /chat

Request body:

```json
{
  "session_id": "optional-existing-session-id",
  "message": "What is LensPilot?"
}
```

Response `200 OK`:

```json
{
  "reply": "LensPilot is an AI-powered browser-based platform that lets customers virtually try on contact lenses using real-time iris segmentation and augmented reality.",
  "sources": [
    {
      "document_id": 2,
      "document_title": "Product Overview",
      "category": "Product",
      "audience": "public",
      "source": "LensPilot Knowledge Base v1",
      "similarity": 0.83
    }
  ],
  "session_id": "3f6e3a4f-0f68-4b49-9b6d-df0d88eab123"
}
```

Expected errors:

- `401` - missing or invalid API key, only if `API_KEY` is configured
- `429` - too many `/chat` or `/ingest` requests from the same client
- `422` - invalid request body
- `502` - LLM provider failure
- `503` - retrieval or database lookup failure
- `500` - unexpected server error

Known FAQ/workflow/role questions and hard refusal cases are answered from
approved local LensPilot knowledge before the backend calls Gemini. This keeps
patch validation stable when Gemini is temporarily rate-limited; other
LensPilot questions still use retrieval plus the configured chat model.

Every response includes `x-request-id` for support/debugging.

## POST /ingest

Triggers ingestion of documents in `INGESTION_DOCS_DIR`.

Response `200 OK`:

```json
{
  "status": "ok",
  "documents_inserted": 3,
  "documents_skipped_unchanged": 0,
  "chunks_inserted": 11
}
```
