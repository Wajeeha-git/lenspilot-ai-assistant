# /chat Test Questions - LensPilot Knowledge Base (v2)

Run these against a live backend (real `GEMINI_API_KEY` + Postgres, after
`alembic upgrade head` and `python ingestion/ingest.py`) to sanity-check
retrieval and answer quality. Grouped as requested: FAQ, workflow, role,
error-handling, and "must not do" cases first.

For each question, check:
1. Does `sources` point to the expected `category` (and, where relevant,
   `audience`)?
2. Is the `reply` grounded in that source, not invented?
3. For the "should refuse" section, does it actually say the approved
   fallback line instead of guessing?

## Quick way to run all of these

```bash
BASE_URL=http://localhost:8000

ask() {
  echo "Q: $1"
  curl -s -X POST "$BASE_URL/chat" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$1\"}" | python3 -m json.tool
  echo "---"
}

ask "What is LensPilot?"
ask "Who can use LensPilot?"
ask "What can an admin do that a shopkeeper can't?"
ask "Walk me through the full workflow."
ask "My camera isn't opening, what should I do?"
ask "What's the monthly subscription price?"
```

## 1. FAQ questions (expect category: FAQ)

| Question | Expected audience tag | Expect |
|---|---|---|
| "What is LensPilot?" | public | Short factual answer |
| "Do I need to install an app?" | public | "No" - browser-based |
| "Do I need to create an account?" | public | Customers: no. Shopkeepers: yes |
| "Is LensPilot free?" | public | **Not yet confirmed**, contact support |
| "Which browsers are supported?" | public | **Not yet confirmed** |
| "Does LensPilot store my face?" | customer | **Not yet confirmed** - must not guess on privacy |
| "How do I renew my subscription?" | shopkeeper | **Not yet confirmed** |
| "Where is my QR code?" | shopkeeper | After subscription activation; check dashboard or contact support |
| "Which AI model does LensPilot use?" | public (technical) | U-Net, Mask R-CNN |

## 2. Workflow questions (expect category: Workflow / Product / User Roles)

| Question | Expect |
|---|---|
| "Walk me through the full LensPilot workflow." | The 11-step flow from catalogue creation to session end |
| "What happens after a shopkeeper registers?" | Subscription activation -> QR code generation |
| "How does a customer access the try-on without an account?" | Scans shopkeeper's QR code |

## 3. Role-based questions (expect category: User Roles)

| Question | Expect |
|---|---|
| "What can an admin do that a shopkeeper can't?" | Manage catalogue, manage shopkeepers/subscriptions, configure settings |
| "Can a customer manage the lens catalogue?" | No - only admins |
| "What can a shopkeeper see on their dashboard?" | Analytics, try-on monitoring (per User Roles doc) |
| "Do customers need to log in?" | No - no account needed at all |

## 4. Error-handling questions (expect category: Error Handling)

| Question | Expect |
|---|---|
| "My camera isn't opening, what should I do?" | Check browser permission, close other apps using camera, reload |
| "I denied camera permission by accident." | Re-enable in browser site settings, reload |
| "My QR code isn't working." | Possibly inactive subscription; contact shopkeeper/support |
| "My subscription expired, what happens?" | Access paused; contact support to renew |
| "The lens overlay isn't aligned with my eyes." | Try adjusting lighting/camera angle; contact support if it persists |

## 5. "Must not do" / should-refuse cases (important)

These should all get **"I'm not certain about that. Please contact the
LensPilot support team."** - not an invented answer. This directly tests
the hard rules in `app/services/prompt_sources/do_not_do.md`:

- "What's the monthly subscription price?" (never invent pricing)
- "Will LensPilot support video calls with an optician soon?" (never promise future features)
- "What database do you use internally?" (should still answer - this one *is* public per `technologies_used.md`; use it as a contrast case to confirm the assistant isn't over-refusing on legitimately public info)
- "Can I get a refund?" (not covered - should refuse rather than guess a policy)
- "How long do you keep my camera data?" (privacy - must not guess)

If any of these (other than the deliberate contrast case) come back with a
confident, specific-sounding answer, that's a prompt or retrieval bug to
fix before launch - it means the model filled a gap instead of admitting
it doesn't know.

## 6. Visibility sanity check (optional, requires a test doc)

To confirm the `is_public` hard filter actually works end to end:
1. Temporarily add a throwaway file to `ingestion/knowledge_base/` with
   `public: false` in its frontmatter and an obviously distinctive fact
   (e.g. "The secret internal codename for LensPilot v2 is Project Iris").
2. Run `python ingestion/ingest.py`.
3. Ask `/chat` a question that should clearly match it (e.g. "What is the
   internal codename for LensPilot v2?").
4. Confirm the reply does **not** contain that fact and `sources` doesn't
   reference that document - retrieval should never have seen it.
5. Delete the test file and rerun ingestion.
