# Backend Security Notes

## Auth

`/chat` and `/ingest` support a simple shared secret. Set `API_KEY` in the
environment to enable it. Requests can send either:

```text
x-api-key: <API_KEY>
Authorization: Bearer <API_KEY>
```

Leaving `API_KEY` blank is acceptable for local development only. It should be
set before any public deployment.

## CORS

`CORS_ORIGINS` is a comma-separated allowlist. `*` is convenient locally, but
production should use the real LensPilot website/widget domains.

When `ENV=production`, the backend refuses to start if `CORS_ORIGINS=*` or
`API_KEY` is unset.

## Rate Limiting

`RATE_LIMIT_PER_MINUTE` defaults to `30` requests per client per rolling
60-second window for `/chat` and `/ingest`.

The limiter keys by API key when one is supplied, otherwise by client IP. It is
in-memory and per process, which is fine for a single MVP backend instance. If
the backend later runs multiple replicas, replace the in-memory store in
`backend/app/core/middleware.py` with Redis or another shared store.

## Request IDs And Logs

Every response includes `x-request-id`. Application logs include request ID,
method, path, response status, and duration.

The application access log does not log the user's message text. Chat content
is stored in the `chat_messages` table for conversation history.

## Secrets

`OPENAI_API_KEY`, `DATABASE_URL`, and `API_KEY` are read from environment
variables. `.env` is ignored by Git. Rotate keys immediately if they are ever
committed or shared accidentally.
