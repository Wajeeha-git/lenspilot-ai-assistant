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

**`X-Forwarded-For` trust:** the limiter reads this header to find the real
client IP behind a proxy/load balancer. This is only safe if the backend sits
behind infrastructure that sets or overwrites this header itself (most PaaS
load balancers, for example Render, Railway, Fly, or an nginx/ALB in front of
the container, do this). If the backend container is ever exposed directly to
the internet with no proxy in front of it, a client can set this header
themselves to dodge the per-IP limit. Confirm your deployment target sits
behind a proxy before relying on this for abuse protection; otherwise fall
back to `request.client.host` only.

## Request IDs And Logs

Every response includes `x-request-id`. Application logs include request ID,
method, path, response status, and duration.

The application access log does not log the user's message text. Chat content
is stored in the `chat_messages` table for conversation history.

## Knowledge Base Visibility

Each ingested document has an `is_public` flag (from its frontmatter's
`public:` field, default `true`). Retrieval (`app/services/retrieval.py`)
hard-filters on `is_public = true` at the database query level -- a
document marked `public: false` is never eligible to be returned to
`/chat`, regardless of how similar it is to the question. This is the
actual enforcement mechanism for keeping internal-only content out of
customer-facing answers; it isn't just a label on the document.

`category` and `audience` are also stored per document and returned in
`/chat`'s `sources` for transparency, but are not currently used as a hard
filter -- a shopkeeper-audience doc can still answer a customer's question
about shopkeepers, for example. If stricter audience-based filtering is
needed later, it's a query change in `retrieval.py`, not a re-ingestion.

## Secrets

`OPENAI_API_KEY`, `DATABASE_URL`, and `API_KEY` are read from environment
variables. `.env` is ignored by Git. Rotate keys immediately if they are ever
committed or shared accidentally.
