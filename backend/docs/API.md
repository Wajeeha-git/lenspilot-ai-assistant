# LensPilot Brain API Contract

Base URL for integrations:

```text
http://localhost:8000/api/v1
```

For local smoke tests, the same endpoints are also exposed without the
`/api/v1` prefix.

All responses are JSON. FastAPI validation/auth errors use the standard
`{"detail": ...}` shape.

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
  "message": "How much does LensPilot cost?"
}
```

Response `200 OK`:

```json
{
  "reply": "LensPilot offers a 14-day free trial...",
  "sources": [
    {
      "document_id": 2,
      "document_title": "Faq",
      "source": "FAQ",
      "similarity": 0.83
    }
  ],
  "session_id": "3f6e3a4f-0f68-4b49-9b6d-df0d88eab123"
}
```

Expected errors:

- `401` - missing or invalid API key, only if `API_KEY` is configured
- `422` - invalid request body
- `502` - LLM provider failure
- `503` - retrieval or database lookup failure
- `500` - unexpected server error

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
