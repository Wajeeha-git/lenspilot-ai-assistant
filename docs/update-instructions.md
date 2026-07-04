# LensPilot Knowledge Base — Update Instructions

This guide explains how to add new content, re-ingest documents, and verify 
quality for the LensPilot AI Assistant's knowledge base.

---

## 1. How to Add a New Document

1. Create a new `.md` file inside the `data/` folder.
   - Use a clear, topic-based filename (e.g., `refund_policy.md`, `pricing.md`).
   - Keep one topic per file — don't mix multiple unrelated topics in one document.

2. Follow the existing formatting style:
   - Use `#` for the main title and `##` for sections.
   - Write in clear, simple language — avoid technical jargon where possible.
   - Keep sections short and specific (this helps the AI retrieve accurate answers).

3. If the document should be excluded from customer-facing answers (internal-only 
   content), mark it accordingly in the frontmatter (check with the backend team 
   for the exact `public: true/false` format used in `backend/ingestion/knowledge_base/`).

4. Save the file, then follow the Git workflow:
```bash
   git checkout main
   git pull origin main
   git checkout -b knowledge/<short-description-of-update>
   git add data/<new-file>.md
   git commit -m "Add [topic] documentation"
   git push origin knowledge/<short-description-of-update>
```
5. Open a Pull Request on GitHub for review before merging into `main`.

---

## 2. How to Re-Ingest Documents

After adding or updating documents, the backend needs to "re-learn" them:

1. Coordinate with the backend team member, since ingestion is run from their side.
2. As documented in `backend/docs/BACKEND_SETUP.md`, the ingestion script is run with:
```bash
   python ingestion/ingest.py
```
3. Alternatively, for smaller updates, the `/ingest` API endpoint can be used 
   (see `docs/API.md` for details) — but this is intended for admin/dev use only.
4. After ingestion, confirm the new document appears in the `sources` field of 
   a relevant `/chat` response.

---

## 3. How to Check Quality

After adding new content or updating the prompt, verify quality using this process:

1. Open the relevant file(s) in `tests/` (organized by category: general, 
   customer, shopkeeper, policy, pricing, etc.)
2. Pick a few sample questions related to the new content.
3. Test them against the assistant (via a chatbot with the knowledge base 
   attached, or the live `/chat` endpoint).
4. Compare the actual answer to the expected answer using this checklist:
   - Does it answer only from the docs (no invented information)?
   - Does it correctly refuse when information isn't available?
   - Is the tone friendly, professional, and concise?
   - Does it stay in scope (LensPilot-related only)?
5. Log results in a new file under `tests/results/` following the existing format:
```markdown
   **Question:** ...
   **Real Answer:** ...
   **Given Answer:** ...
   **Match?** ✅ perfect match/ ⚠️ partial match / ❌ no match
```
6. If patterns of failure appear (e.g., repeated over-caution, wrong tone), 
   update `docs/prompt-guidelines.md` accordingly and re-test.

---

## Reference Files
- `data/` — knowledge base source documents
- `docs/prompt-guidelines.md` — assistant behavior rules
- `docs/API.md` — API contract (request/response format)
- `tests/` — test questions and results by category