# Frontend Integration Checklist (Day 5 Review)

Reviewed the backend's API.md contract. Summary for frontend team:

## What the API provides:
- `reply` — the assistant's answer text
- `sources` — list of documents used to generate the answer (title, category, similarity score)
- `session_id` — must be saved and reused for follow-up messages in the same conversation
- `error` — returned as `{ "error": "message" }` with HTTP status codes (401, 422, 429, 500, 502, 503)

## What frontend needs to handle on its own:
- Loading state (show "typing..." while waiting for the API response)
- Displaying a user-friendly message when an `error` is received
- Storing and sending `session_id` with follow-up messages

## Status: ✅ API contract is stable and sufficient for the widget.