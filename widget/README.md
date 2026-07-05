# LensPilot Widget — Member 3 (Frontend/Widget) deliverable

A real React + Vite + Tailwind project (not a single-file demo) containing
the embeddable chat widget and the view-only demo page around it.

## Project structure

```
lenspilot-widget/
├─ public/
│  └─ logo.png                  ← real LensPilot logo
├─ src/
│  ├─ components/
│  │  └─ ChatWidget.jsx         ← Member 3: the widget itself
│  ├─ services/
│  │  └─ chatService.js         ← Member 1: real /chat call goes here
│  ├─ mock/
│  │  └─ knowledgeBase.js       ← Member 2: content/prompt/mock answers
│  ├─ App.jsx                   ← demo landing page (view-only) + widget
│  ├─ main.jsx                  ← React entry point
│  └─ index.css                 ← Tailwind entry + small custom animations
├─ index.html
├─ tailwind.config.js
├─ postcss.config.js
├─ vite.config.js
├─ .env.example
└─ package.json
```

## Setup

```bash
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

```bash
npm run build      # production build -> dist/
npm run preview    # preview the production build locally
```

## What's already working

- Floating chat button + panel (open/close)
- **Free-text input** — the user can type any question, not just the
  suggested chips. Chips are just shortcuts; the same `send()` function
  handles both.
- Loading state (typing-dots indicator) while waiting for a reply
- Error state with a **Retry** button
- Source pills under assistant replies
- Fully responsive — one set of Tailwind classes with breakpoint
  variants (`sm:`, `lg:`), no separate mobile version to maintain
- Mock replies via keyword/overlap matching in `src/mock/knowledgeBase.js`,
  with an honest "I don't know" fallback when nothing matches (mirrors
  the real assistant's "say when unsure" rule)

## Step 31 — Embed instructions

This project is currently structured as a full page (widget + demo site
together) for development. To embed **just the widget** on another site
once you're ready:

**Option A — embed the built widget as a script (recommended for other sites)**
1. Create a small entry file, e.g. `src/embed.jsx`:
   ```jsx
   import ReactDOM from "react-dom/client";
   import ChatWidget from "./components/ChatWidget.jsx";
   import "./index.css";

   const mount = document.createElement("div");
   document.body.appendChild(mount);
   ReactDOM.createRoot(mount).render(<ChatWidget />);
   ```
2. Add a Vite library build target for it (or use `vite build --config vite.embed.config.js`)
   so it outputs a single `lenspilot-widget.js` + `lenspilot-widget.css`.
3. On any host site, add before `</body>`:
   ```html
   <link rel="stylesheet" href="https://your-cdn.com/lenspilot-widget.css" />
   <script src="https://your-cdn.com/lenspilot-widget.js"></script>
   ```
   The widget mounts itself — no extra markup needed on the host page.

**Option B — just use this repo as the demo site**
If LensPilot is only ever shown on its own demo/marketing site (not embedded
elsewhere), you don't need Option A at all — just deploy `dist/` after
`npm run build` (e.g. to Vercel/Netlify) and the widget is already on the page.

## Step 32 — How to change the API URL

The widget never hardcodes a URL. It reads `VITE_API_BASE_URL` from your
environment:

1. Copy `.env.example` to `.env` (or `.env.local` for a value that
   shouldn't be committed):
   ```bash
   cp .env.example .env
   ```
2. Set it to wherever Member 1's backend is running:
   ```
   VITE_API_BASE_URL=https://api.lenspilot.example.com
   ```
3. Restart `npm run dev` (Vite only reads `.env` files at startup).

For local development against a backend on a different port, you can
alternatively use the commented-out proxy block in `vite.config.js` to
avoid CORS entirely — point it at your local FastAPI server and call
`/api/chat` from the frontend.

## Connecting to the real backend (Member 1)

Everything backend-related lives in **`src/services/chatService.js`** —
that's the only file that should need to change:

1. Confirm the request/response shape against `docs/API.md`.
2. Set `CONFIG.USE_MOCK = false` in that file.
3. Set `VITE_API_BASE_URL` as above.

The real call is already written (commented out) inside `sendMessage()`:

```js
const res = await fetch(`${CONFIG.API_BASE_URL}/chat`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message, session_id: ChatService.sessionId }),
});
```

It sends `message` + `session_id` (Step 18) and expects
`{ reply, sources, error }` back, which `ChatWidget.jsx` already knows
how to render (Step 19) — including the sources pills and error/retry UI.

## Updating content (Member 2)

Edit `src/mock/knowledgeBase.js` only:
- `ASSISTANT_IDENTITY` — name, greeting, fallback "I don't know" message
- `SUGGESTED_QUESTIONS` — the quick-reply chips
- `KNOWLEDGE_BASE` — array of `{ keywords, answer, source }` mock answers

No React/JS framework knowledge required — it's plain arrays/objects.
