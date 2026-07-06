# Frontend Integration Checklist

Reviewed the backend API contract. Summary for the frontend team:

## What The API Provides

- `reply` - the assistant answer text.
- `sources` - documents used to generate the answer.
- `session_id` - saved and reused for follow-up messages in the same conversation.
- `error` - returned as `{ "error": "message" }` with HTTP status codes.

## What The Frontend Handles

- Loading state while waiting for the API response.
- User-friendly message when an `error` is received.
- Storing and sending `session_id` with follow-up messages.

## Status

The API contract is stable and sufficient for the widget.
