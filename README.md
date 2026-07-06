# LensPilot AI Assistant

LensPilot AI Assistant is the support and product-guidance assistant for the
LensPilot virtual contact lens try-on platform. The project includes a FastAPI
backend, a React chat widget, curated LensPilot knowledge-base documents, prompt
rules, migrations, tests, and GitHub workflow documentation.

## Repository

- GitHub: https://github.com/Wajeeha-git/lenspilot-ai-assistant
- Stable branch: `main`
- Integration branch: `knowledge/frontend-support`

## Project Structure

```text
lenspilot-ai-assistant/
|-- backend/      FastAPI API, RAG services, Gemini integration, migrations, tests
|-- widget/       React/Vite chat widget used by the demo frontend
|-- demo-site/    Demo host notes for the widget
|-- docs/         API contract, security notes, workflow, reports, demo questions
|-- data/         Data documentation and seed-data area
|-- .github/      Issue templates, PR template, and CI workflow
|-- CODEOWNERS    Review ownership by project area
`-- CONTRIBUTING.md
```

## Current Status

The final integration branch contains the working backend API, the connected
frontend widget, the LensPilot knowledge base, prompt rules, deterministic
fallback answers for approved demo questions, refusal behavior, and automated
tests.

Validated locally:

- Backend test suite: `python -m pytest`
- Widget production build: `npm run build`
- Live chat validation: `run-chat-tests.ps1`
- Frontend/backend connection: widget calls `http://127.0.0.1:8000/api/v1/chat`

## Local Development

### Backend

```powershell
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

Backend endpoints:

- API status: `http://127.0.0.1:8000/api/v1/health`
- API docs: `http://127.0.0.1:8000/docs`
- Chat endpoint: `POST http://127.0.0.1:8000/api/v1/chat`

### Widget

```powershell
cd widget
npm install
npm run dev
```

Frontend URL:

- `http://127.0.0.1:5173/`

## Documentation

- [Project Report](docs/PROJECT_REPORT.md)
- [Demo Questions](docs/DEMO_QUESTIONS.md)
- [API Contract](docs/API.md)
- [Prompt Guidelines](docs/prompt-guidelines.md)
- [Security](docs/SECURITY.md)
- [Team Workflow](docs/WORKFLOW.md)
- [Branch Protection](docs/BRANCH_PROTECTION.md)
- [Contributing](CONTRIBUTING.md)

## GitHub Workflow

The team workflow is:

1. Keep `main` stable.
2. Create focused `feature/...`, `fix/...`, `docs/...`, or `chore/...` branches.
3. Run tests locally before pushing.
4. Open a Pull Request.
5. Review and resolve comments.
6. Merge only after the branch is stable.
7. Delete merged branches after the work is safely on `main`.

## License

Private repository. All rights reserved.
