# Team Workflow

This is the standard workflow for keeping the repository professional and
stable.

## Daily Start

1. Pull latest `main`.
2. Create or update your task branch.
3. Confirm task ownership.
4. Check whether your work touches shared API, prompt, or schema files.

```powershell
git checkout main
git pull origin main
git checkout -b feature/your-task
```

## During Work

1. Make focused commits.
2. Keep frontend/backend contracts aligned with `docs/API.md`.
3. Keep prompt and knowledge-base changes in their documented folders.
4. Avoid committing local-only files, generated outputs, or secrets.

## Before PR

1. Run backend tests when backend, prompt, docs ingestion, or API behavior changed.
2. Run widget build when frontend/widget behavior changed.
3. Run the chat validation script when assistant behavior changed.
4. Push the branch and open a PR.

```powershell
cd backend
.\venv\Scripts\python -m pytest
```

```powershell
cd widget
npm run build
```

```powershell
.\run-chat-tests.ps1
```

## Review And Merge

1. Review the PR.
2. Resolve comments.
3. Confirm CI is green.
4. Merge into `main`.
5. Pull updated `main`.
6. Delete the merged branch after the work is safely on `main`.

## API Change Protocol

Follow this order for endpoint or response-shape changes:

1. Update `docs/API.md`.
2. Update backend schemas/routes.
3. Update frontend service calls.
4. Add or update tests.
5. Run backend and frontend verification.

## Branch Reference

| Work type | Branch format | Example |
| --- | --- | --- |
| Feature | `feature/<short-desc>` | `feature/chat-widget-api` |
| Bug fix | `fix/<short-desc>` | `fix/refusal-chip-routing` |
| Docs | `docs/<short-desc>` | `docs/project-report` |
| Refactor | `refactor/<short-desc>` | `refactor/prompt-loader` |
| Maintenance | `chore/<short-desc>` | `chore/ci-cleanup` |
