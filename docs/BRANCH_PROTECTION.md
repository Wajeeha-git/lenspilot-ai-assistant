# Branch Protection Setup Guide

> ⚠️ Branch protection on **private repositories** requires **GitHub Pro** (or GitHub Team/Enterprise).
> This guide documents exactly what to enable once you upgrade.

---

## How to Protect the `main` Branch

### Step 1 — Open branch settings

1. Go to your repo: https://github.com/Wajeeha-git/lenspilot-ai-assistant
2. Click **Settings** (top menu)
3. Click **Branches** (left sidebar)
4. Under **Branch protection rules**, click **Add rule**

---

### Step 2 — Configure the rule

**Branch name pattern:** `main`

Enable these settings:

| Setting | Enable? |
|---|---|
| ✅ Require a pull request before merging | YES |
| ✅ Require approvals | YES — set to **1** |
| ✅ Dismiss stale pull request approvals when new commits are pushed | YES |
| ✅ Require review from Code Owners | YES |
| ✅ Require status checks to pass before merging | YES |
| ✅ Require branches to be up to date before merging | YES |
| ✅ Require conversation resolution before merging | YES |
| ✅ Do not allow bypassing the above settings | YES |
| ❌ Allow force pushes | NO |
| ❌ Allow deletions | NO |

---

### Step 3 — Save

Click **Create** at the bottom of the page.

---

## Verification Checklist

After saving, verify:

- [ ] Go to the repo and try pushing directly to main — it should be blocked
- [ ] Open a test PR — it should require review before merge
- [ ] Force push should be rejected

---

## Alternative: GitHub Rulesets (Free Plan)

If you stay on the free plan, GitHub **Rulesets** are only available for public repos or Pro/Team.
The manual team rules in `CONTRIBUTING.md` serve as the social contract until then.

---

## CODEOWNERS — How to Update

The `CODEOWNERS` file is at the root of the repo. Replace the placeholder usernames with real GitHub usernames:

```
# Before:
/backend/   @backend-owner

# After (example):
/backend/   @jane-doe
```

Commit and push the updated `CODEOWNERS` — GitHub will automatically request reviews from owners when their files are touched in a PR.
