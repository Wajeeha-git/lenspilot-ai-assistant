# Project Report

## Repository Links

- GitHub repository: https://github.com/Wajeeha-git/lenspilot-ai-assistant
- Stable branch: https://github.com/Wajeeha-git/lenspilot-ai-assistant/tree/main
- Integration branch: https://github.com/Wajeeha-git/lenspilot-ai-assistant/tree/knowledge/frontend-support

## Current Status

The LensPilot AI Assistant is integrated and working locally. The backend API,
React widget, LensPilot knowledge base, prompt rules, deterministic fallback,
tests, and documentation are in place. The widget calls the backend at
`/api/v1/chat`, and the assistant returns grounded answers with source metadata.

The project is ready to be merged into `main` after the final PR/merge step and
successful verification.

## Member Roles And Completed Work

### Member 01 - Backend/API

Member 01 owns the FastAPI backend, API contract, database models, migrations,
retrieval pipeline, Gemini integration, rate-limit handling, and backend tests.

Completed work:

- Built `/api/v1/health`, `/api/v1/chat`, and `/api/v1/ingest`.
- Added session/message persistence models.
- Added document and chunk models for RAG retrieval.
- Added Alembic migrations, including document metadata.
- Added Gemini chat and embedding services.
- Added retry behavior for provider rate limits.
- Added local deterministic LensPilot fallback for approved FAQ, workflow,
  role, troubleshooting, refusal, and demo cases.
- Added error envelopes and security/rate-limit tests.
- Verified backend tests pass locally.

### Member 02 - Knowledge/Prompt

Member 02 owns LensPilot documents, prompt rules, assistant tone, refusal
behavior, and validation questions.

Completed work:

- Added LensPilot knowledge-base topic files under
  `backend/ingestion/knowledge_base/`.
- Added product, workflow, role, technical, FAQ, AI-feature, business-rule, and
  troubleshooting content.
- Added prompt source files under `backend/app/services/prompt_sources/`.
- Defined assistant identity, tone, and hard refusal rules.
- Added prompt guidance documentation.
- Added expanded chat-test coverage for answer, refusal, and out-of-scope
  behavior.

### Member 03 - Frontend/Widget

Member 03 owns the React/Vite widget UI and user interaction.

Completed work:

- Built the chat widget UI.
- Added greeting, suggested-question chips, message bubbles, source chips,
  loading state, retry behavior, and input form.
- Connected the widget to the backend by default through `VITE_API_BASE_URL`.
- Kept mock mode available only when explicitly enabled with `VITE_USE_MOCK=true`.
- Updated the suggested questions to LensPilot-specific demo-safe prompts.
- Verified the widget production build passes.

## How The Assistant Works

The assistant uses a grounded RAG design:

1. The user sends a message from the widget.
2. The widget calls `POST /api/v1/chat`.
3. The backend creates or reuses a chat session.
4. Known approved LensPilot questions are answered locally without calling the
   external model. This protects demo stability and avoids unnecessary rate-limit
   failures.
5. For other in-scope questions, the backend retrieves relevant document chunks
   from PostgreSQL/pgvector.
6. The prompt builder loads the prompt-source files:
   - `system_prompt.md`
   - `tone_and_personality.md`
   - `do_not_do.md`
7. The retrieved context and prompt rules are sent to Gemini.
8. The assistant returns a concise answer and source metadata.
9. Unknown, unsupported, private, pricing, refund, policy, and future-feature
   questions use the approved refusal text instead of invented answers.

## Knowledge Base Integration

LensPilot documents are stored as topic files in
`backend/ingestion/knowledge_base/`. The ingestion pipeline chunks the documents,
embeds the chunks, and stores them in the database with metadata such as title,
category, source, audience, and public/private status.

This means answers are not based on random model knowledge. The assistant is
grounded in LensPilot-provided content and returns source metadata to the widget.

## Prompt And Refusal Design

Prompt rules are not ingested as ordinary retrievable documents. They are loaded
into the system prompt on every model call so they apply consistently to all
questions.

Important rules:

- Answer only from LensPilot context.
- Do not invent subscription prices.
- Do not promise future features.
- Do not expose confidential/internal information.
- Do not guess privacy, refund, retention, or policy answers.
- Use the exact approved fallback when the answer is not confirmed.
- Keep tone friendly, professional, concise, and easy to understand.

## Proof That It Works

Local verification completed:

- Backend tests: `python -m pytest`
- Widget build: `npm run build`
- Live API check: `POST /api/v1/chat`
- Expanded chat validation: `run-chat-tests.ps1`
- Suggested chip fix verified with both old and new chip text.

Important live validation result from the current integration work:

- 105 assistant questions tested.
- 0 API errors.
- 0 validation failures.
- 41 of 41 refusal-expected questions refused correctly.

## Professional GitHub Workflow

The intended team workflow is:

1. Keep `main` stable.
2. Use feature branches for work.
3. Open Pull Requests for review.
4. Run tests before merge.
5. Merge only stable reviewed code into `main`.
6. Delete merged work branches after the final code is safely on `main`.

Recommended branch layout:

- `main` - stable final branch.
- `feature/backend-api` - backend/API work.
- `feature/widget-frontend` - widget/UI work.
- `feature/knowledge-prompt` - knowledge base and prompt work.
- `knowledge/frontend-support` - current final integration branch.

## Remaining Operational Notes

- Configure branch protection or GitHub rulesets for `main`.
- Require the CI workflow before merging.
- Keep `.env` files out of Git.
- Use `docs/API.md` as the frontend/backend contract.
- Use `docs/DEMO_QUESTIONS.md` for video recording.
