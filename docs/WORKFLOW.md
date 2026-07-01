# Daily Team Workflow — LensPilot AI Assistant

> Follow these routines every day to keep the repo clean, avoid conflicts, and ship safely.

---

## 🌅 Every Morning (Start of Day)

### Step 1 — Sync with main

Always start by pulling the latest code:

```bash
git checkout main
git pull origin main
```

Then update your feature branch if you have one open:

```bash
git checkout feature/your-branch
git rebase main
```

### Step 2 — Check open issues

1. Go to [Issues](../../issues) on GitHub.
2. Check if any issues are unassigned — assign them to the right person.
3. Confirm no two people are working on the same file or feature.
4. If a conflict is possible, communicate in team chat first.

### Step 3 — Confirm task ownership

Before writing any code, make sure:

- [ ] Your issue is assigned to you
- [ ] Your branch is created from the latest `main`
- [ ] No one else is editing the same file(s)

---

## 🌆 Every Evening (End of Day)

### Step 4 — Review open PRs

1. Go to [Pull Requests](../../pulls) on GitHub.
2. Review any PRs that are waiting for approval.
3. Leave review comments or approve.
4. Merge approved PRs (all checks must pass).

### Step 5 — Clean up merged branches

After merging a PR, delete the branch:

```bash
# Locally
git branch -d feature/your-branch

# On remote (or use GitHub UI — it prompts after merge)
git push origin --delete feature/your-branch
```

### Step 6 — Update issues

After merging:
- Close the issue linked to the PR.
- Add any follow-up notes if needed.
- Check if new tasks need to be created.

---

## ⚠️ If Schema or API Changes Are Needed (Steps 14–16)

**Follow this order strictly. No exceptions.**

1. **Announce first** — Post in team chat: _"I need to change [endpoint/field] because [reason]."_ Wait for acknowledgement.
2. **Update docs first** — Edit `docs/API.md` before touching any code. Commit the doc change separately.
3. **Then update code** — Backend and frontend changes come after the spec is agreed upon.
4. **Notify again** — Once merged, post in team chat: _"API spec updated — please pull latest main."_

> ⛔ Never change the API contract in code without updating `docs/API.md` first.

---

## 🌿 Branch Quick Reference

| Task type | Branch name format | Example |
|---|---|---|
| New feature | `feature/<short-desc>` | `feature/add-chat-history` |
| Bug fix | `fix/<short-desc>` | `fix/widget-overflow` |
| Documentation | `docs/<short-desc>` | `docs/update-api-spec` |
| Refactor | `refactor/<short-desc>` | `refactor/chat-engine` |
| Maintenance | `chore/<short-desc>` | `chore/update-dependencies` |

---

## ✅ PR Checklist (Before Opening a PR)

- [ ] Branched from latest `main`
- [ ] Rebased/merged with latest `main` before PR
- [ ] PR is small (one logical change only)
- [ ] Related issue is linked (`Closes #<issue-number>`)
- [ ] `docs/API.md` updated if API changed
- [ ] Tested locally
- [ ] No secrets or `.env` files committed

---

## 👥 Adding New Team Members

Only the repo owner can add collaborators:

1. Go to **Settings → Collaborators** on GitHub.
2. Click **Add people**.
3. Enter the GitHub username — only invite people explicitly approved.
4. Set role: **Write** (for contributors) or **Admin** (for leads).
5. Update `CODEOWNERS` with their GitHub username.

> New members should read `CONTRIBUTING.md` and `docs/API.md` before writing any code.
