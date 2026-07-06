# Contributing

Use this workflow to keep the LensPilot AI Assistant repository clean,
reviewable, and safe for team collaboration.

## Branch Rules

1. Keep `main` stable and merge-ready.
2. Create one branch per task.
3. Branch from the latest `main`.
4. Use clear branch prefixes:
   - `feature/<short-description>`
   - `fix/<short-description>`
   - `docs/<short-description>`
   - `refactor/<short-description>`
   - `chore/<short-description>`

Example:

```powershell
git checkout main
git pull origin main
git checkout -b feature/chat-widget-api
```

## Pull Request Rules

1. Do not push directly to `main`.
2. Keep each PR focused on one logical change.
3. Link the related issue when one exists.
4. Explain what changed, why it changed, and how it was tested.
5. Update `docs/API.md` before changing backend/frontend API contracts.
6. Wait for review before merging.
7. Merge only when tests pass.

## Shared Files

Ask the team before changing shared repository files:

- `README.md`
- `.env.example`
- `.gitignore`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `docs/API.md`
- `.github/workflows/*`

## Test Checklist

Before opening or merging a PR, run the relevant checks:

```powershell
cd backend
.\venv\Scripts\python -m pytest
```

```powershell
cd widget
npm run build
```

For the live assistant validation:

```powershell
.\run-chat-tests.ps1
```

## Do Not Commit

Keep these out of PRs and `main`:

- Secrets and real `.env` files
- Generated logs and test-output files
- Local troubleshooting scripts
- Half-finished experiments
- Unreviewed API-contract changes
- Build artifacts such as `dist/` and `node_modules/`
