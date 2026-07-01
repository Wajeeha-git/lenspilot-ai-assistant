# LensPilot AI Assistant — API Contract

> **Version:** 1.0.0  
> **Last Updated:** 2026-07-01  
> **Status:** Draft — Do not change without team announcement

---

## Base URL

```
http://localhost:8000/api/v1
```

---

## Endpoints

### 1. `GET /health`

Health check endpoint to verify the API server is running.

**Request:**
```
GET /api/v1/health
```

No headers or body required.

**Response — `200 OK`:**
```json
{
  "status": "ok",
  "timestamp": "2026-07-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "vector_store": "connected",
    "llm": "connected"
  }
}
```

**Response — `503 Service Unavailable`:**
```json
{
  "status": "degraded",
  "timestamp": "2026-07-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "vector_store": "disconnected",
    "llm": "connected"
  }
}
```

---

### 2. `POST /chat`

Send a user message and receive an AI-generated response.

**Request:**
```
POST /api/v1/chat
Content-Type: application/json
Authorization: Bearer <API_KEY>
```

**Request Body:**
```json
{
  "message": "How do I reset my password?",
  "session_id": "sess_abc123",
  "context": {
    "user_id": "user_456",
    "page": "/settings"
  }
}
```

| Field        | Type     | Required | Description                              |
|-------------|----------|----------|------------------------------------------|
| `message`   | `string` | ✅ Yes   | The user's message text                  |
| `session_id`| `string` | ❌ No    | Session ID for conversation continuity   |
| `context`   | `object` | ❌ No    | Additional context (user ID, page, etc.) |

**Response — `200 OK`:**
```json
{
  "reply": "To reset your password, go to Settings > Security > Reset Password.",
  "session_id": "sess_abc123",
  "sources": [
    {
      "title": "Password Reset Guide",
      "chunk_id": "doc_789_chunk_3",
      "relevance_score": 0.94
    }
  ],
  "tokens_used": {
    "prompt": 150,
    "completion": 42,
    "total": 192
  }
}
```

| Field          | Type       | Description                                |
|---------------|------------|--------------------------------------------|
| `reply`       | `string`   | The AI-generated response                  |
| `session_id`  | `string`   | Session ID (created if not provided)       |
| `sources`     | `array`    | Knowledge base chunks used for the answer  |
| `tokens_used` | `object`   | Token usage breakdown                      |

**Response — `400 Bad Request`:**
```json
{
  "error": "validation_error",
  "message": "Field 'message' is required and must be a non-empty string.",
  "code": 400
}
```

**Response — `401 Unauthorized`:**
```json
{
  "error": "unauthorized",
  "message": "Invalid or missing API key.",
  "code": 401
}
```

**Response — `500 Internal Server Error`:**
```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred. Please try again.",
  "code": 500
}
```

---

### 3. `POST /ingest`

Ingest documents into the knowledge base for retrieval-augmented generation (RAG).

**Request:**
```
POST /api/v1/ingest
Content-Type: application/json
Authorization: Bearer <API_KEY>
```

**Request Body:**
```json
{
  "documents": [
    {
      "title": "Password Reset Guide",
      "content": "To reset your password, navigate to Settings > Security...",
      "metadata": {
        "category": "support",
        "source": "help-center",
        "language": "en"
      }
    }
  ],
  "options": {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "overwrite": false
  }
}
```

| Field              | Type      | Required | Description                              |
|-------------------|-----------|----------|------------------------------------------|
| `documents`       | `array`   | ✅ Yes   | Array of documents to ingest             |
| `documents[].title`   | `string` | ✅ Yes | Document title                           |
| `documents[].content` | `string` | ✅ Yes | Document text content                    |
| `documents[].metadata`| `object` | ❌ No  | Metadata tags (category, source, etc.)   |
| `options`         | `object`  | ❌ No    | Ingestion configuration                  |
| `options.chunk_size`   | `number` | ❌ No | Characters per chunk (default: 500)      |
| `options.chunk_overlap`| `number` | ❌ No | Overlap between chunks (default: 50)     |
| `options.overwrite`    | `boolean`| ❌ No | Overwrite existing docs (default: false) |

**Response — `200 OK`:**
```json
{
  "status": "success",
  "documents_ingested": 1,
  "chunks_created": 5,
  "processing_time_ms": 1230
}
```

**Response — `400 Bad Request`:**
```json
{
  "error": "validation_error",
  "message": "Field 'documents' must be a non-empty array.",
  "code": 400
}
```

**Response — `401 Unauthorized`:**
```json
{
  "error": "unauthorized",
  "message": "Invalid or missing API key.",
  "code": 401
}
```

---

## Error Format (Standard)

All error responses follow this shape:

```json
{
  "error": "<error_type>",
  "message": "<human_readable_description>",
  "code": <http_status_code>
}
```

| Error Type          | Code | When                                     |
|--------------------|------|------------------------------------------|
| `validation_error` | 400  | Missing or invalid request fields        |
| `unauthorized`     | 401  | Invalid or missing API key               |
| `not_found`        | 404  | Endpoint or resource not found           |
| `rate_limited`     | 429  | Too many requests                        |
| `internal_error`   | 500  | Unexpected server error                  |

---

## Notes

- All timestamps are in **ISO 8601 UTC** format.
- All endpoints return **JSON** (`Content-Type: application/json`).
- The `Authorization` header uses **Bearer token** format.
- Changes to this spec must be **announced in team chat** and **updated here first** before any code changes.
