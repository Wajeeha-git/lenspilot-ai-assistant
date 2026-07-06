# Branch Protection

Use branch protection or repository rulesets so `main` stays stable.

## Recommended Rule For `main`

Enable these settings in GitHub:

| Setting | Recommendation |
| --- | --- |
| Require a pull request before merging | Enabled |
| Required approvals | At least 1 |
| Dismiss stale approvals | Enabled |
| Require conversation resolution | Enabled |
| Require status checks | Enabled |
| Require branches to be up to date | Enabled |
| Allow force pushes | Disabled |
| Allow deletions | Disabled |

## Required Checks

Use these checks before merging assistant work:

- Backend tests and migrations
- Widget build
- Manual live chat validation for assistant behavior changes

## CODEOWNERS

`CODEOWNERS` assigns review ownership by project area. Keep GitHub usernames
current so PR review requests go to the right team member.

## Manual Rule Until Protection Is Enabled

If GitHub branch protection is not enabled yet, follow the team rule manually:

1. Work on a branch.
2. Push the branch.
3. Open a PR.
4. Review the PR.
5. Merge only after tests pass.
