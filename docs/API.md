# LensPilot AI Assistant API Contract

Version: 1.0.0
Last updated: 2026-07-02
Status: Draft - announce team-wide before changing this file.

## Base URL

Local development:

```text
http://localhost:8000/api/v1
```

The backend also exposes the same endpoints without `/api/v1` for local
smoke testing, but frontend and website integrations should use the
versioned base URL above.

## Authentication

`GET /health` is public.

If `API_KEY` is configured on the backend, `POST /chat` and `POST /ingest`
must include one of these headers:

```text
x-api-key: <API_KEY>
Authorization: Bearer <API_KEY>
```

If `API_KEY` is blank, auth is disabled for local development.

## GET /health

Checks that the API server is running.

Request:

```http
GET /api/v1/health
```

Response `200 OK`:

```json
{
  "status": "ok"
}
```

## POST /chat

Sends a user question to the LensPilot assistant.

Request:

```http
POST /api/v1/chat
Content-Type: application/json
```

Request body:

```json
{
  "session_id": "optional-existing-session-id",
  "message": "Does LensPilot have a free trial?"
}
```

Fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| `message` | string | Yes | User question. Must be non-empty. |
| `session_id` | string | No | Existing chat session ID. Omit to create a new session. |

Response `200 OK`:

```json
{
  "reply": "LensPilot offers a 14-day free trial...",
  "sources": [
    {
      "document_id": 2,
      "document_title": "FAQ - Customer",
      "category": "FAQ",
      "audience": "customer",
      "source": "LensPilot Knowledge Base v1",
      "similarity": 0.83
    }
  ],
  "session_id": "3f6e3a4f-0f68-4b49-9b6d-df0d88eab123"
}
```

Fields:

| Field | Type | Description |
|---|---|---|
| `reply` | string | Assistant answer generated from retrieved company context. |
| `sources` | array | Document chunks used to ground the response. |
| `session_id` | string | Session ID to reuse for follow-up messages. |

Source fields:

| Field | Type | Description |
|---|---|---|
| `document_id` | number | Database ID of the source document. |
| `document_title` | string | Source document title (from its frontmatter `title:`, or derived from the filename). |
| `category` | string | Topic category, e.g. `FAQ`, `Workflow`, `Error Handling`, `Business Rules`. |
| `audience` | string | Who the doc targets: `public`, `customer`, `shopkeeper`, or `admin`. Informational, not currently used to filter results. |
| `source` | string | Provenance string, e.g. `LensPilot Knowledge Base v1`. |
| `similarity` | number | Retrieval similarity score; higher is better. |

**Note:** only documents marked public in their frontmatter (`public: true`,
the default) are ever eligible for retrieval here - internal-only content
(`public: false`) is hard-excluded before similarity search runs, not just
filtered from the response.

Error responses:

| Status | Meaning |
|---:|---|
| `401` | Missing or invalid API key, when auth is enabled. |
| `429` | Too many `/chat` or `/ingest` requests from the same client. |
| `422` | Invalid request body. |
| `502` | LLM provider failed. |
| `503` | Knowledge retrieval or database lookup failed. |
| `500` | Unexpected server error. |

Error body:

```json
{
  "error": "Human-readable error message"
}
```

Every response includes an `x-request-id` header for support/debugging.

## POST /ingest

Triggers ingestion for documents in the configured backend docs directory.
This is intended for admin/dev use. For larger document sets, run
`python ingestion/ingest.py` from `backend/` instead of calling this endpoint.

Request:

```http
POST /api/v1/ingest
```

Response `200 OK`:

```json
{
  "status": "ok",
  "documents_inserted": 3,
  "documents_skipped_unchanged": 0,
  "chunks_inserted": 11
}
```

## Change Rule

If schema or API behavior changes, update this file first, announce the
change to the team, then update backend/widget code in separate focused PRs.
