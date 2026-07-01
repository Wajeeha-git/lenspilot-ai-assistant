# Contributing to LensPilot AI Assistant

Thank you for contributing! Please follow these rules to keep the codebase clean, safe, and easy to work with.

---

## 🌿 Branch Rules

1. **One branch per task.** Every issue, bug fix, or feature gets its own branch.
2. **Branch naming convention:**
   - `feature/<short-description>` — for new features
   - `fix/<short-description>` — for bug fixes
   - `docs/<short-description>` — for documentation changes
   - `refactor/<short-description>` — for code refactoring
   - `chore/<short-description>` — for maintenance tasks
3. **Always branch from the latest `main`.**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-feature
   ```
4. **Update your branch before opening a PR:**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/my-feature
   git rebase main
   ```

---

## 🔀 Pull Request Rules

1. **No direct commits to `main`.** All changes go through Pull Requests.
2. **Keep PRs small.** One logical change per PR. If a PR is too large, split it.
3. **Every PR needs at least 1 review approval** before merging.
4. **PR title format:** `[area] Short description`
   - Examples: `[backend] Add /chat endpoint`, `[widget] Fix message overflow`, `[docs] Update API spec`
5. **Include a description** explaining what changed and why.
6. **Link the related issue** in the PR description (e.g., `Closes #12`).
7. **All status checks must pass** before merging.

---

## 📁 Shared Files — Ask Before Changing

The following files affect the entire team. **Ask in the team chat before modifying them:**

- `README.md`
- `.env.example`
- `.gitignore`
- `CONTRIBUTING.md`
- `CODEOWNERS`
- `docs/API.md`
- Any CI/CD configuration files

---

## 🐛 Issue Guidelines

- Use the issue templates provided (bug, feature, documentation, backend, frontend, knowledge).
- Assign yourself to the issue before starting work.
- Add appropriate labels.
- Reference the issue number in your branch name and PR.

---

## ✅ Before You Submit a PR

- [ ] My code follows the project style.
- [ ] I've tested my changes locally.
- [ ] I've updated my branch with the latest `main`.
- [ ] I've linked the related issue.
- [ ] My PR is small and focused on one change.
- [ ] I haven't modified shared files without team approval.

---

## 🚫 What NOT to Do

- ❌ Push directly to `main`
- ❌ Force push to shared branches
- ❌ Open a PR without testing locally
- ❌ Change the API contract without updating `docs/API.md` first
- ❌ Modify multiple unrelated things in one PR
