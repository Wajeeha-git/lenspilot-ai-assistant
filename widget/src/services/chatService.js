// ============================================================
// MEMBER 1 — BACKEND / RAG OWNER
// ============================================================
// This is the ONLY file you should need to touch to connect the
// widget to the real backend.
//
// Expected request (confirm exact shape against docs/API.md):
//   POST {API_BASE_URL}/chat
//   { "message": string, "session_id": string }
//
// Expected response:
//   { "reply": string, "sources": string[], "error": string | null }
//
// Until the endpoint is stable, USE_MOCK stays true and this file
// never touches the network — Member 3 can build/demo the whole UI
// with zero backend running.
//
// HOW TO GO LIVE:
//   1. Set VITE_API_BASE_URL in your .env file (see .env.example).
//   2. Flip USE_MOCK to false below.
//   3. That's it — sendMessage() will start calling the real /chat.

import { ASSISTANT_IDENTITY, KNOWLEDGE_BASE } from "../mock/knowledgeBase.js";

export const CONFIG = {
  USE_MOCK: import.meta.env.VITE_USE_MOCK === "true",
  // Reads from .env / .env.local — see .env.example.
  // Defaults to the local FastAPI backend on the documented versioned route.
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
};

let sessionId =
  "session-" + Math.random().toString(36).slice(2, 10) + "-" + Date.now();

function mockMatch(message) {
  const lower = message.toLowerCase();
  const words = lower.split(/\W+/).filter(Boolean);
  return KNOWLEDGE_BASE.find((entry) =>
    entry.keywords.some((k) => {
      if (lower.includes(k)) return true;
      const kWords = k.split(/\W+/).filter(Boolean);
      const overlap = kWords.filter((w) => words.includes(w)).length;
      return overlap > 0 && overlap >= Math.ceil(kWords.length / 2);
    })
  );
}

export const ChatService = {
  get sessionId() {
    return sessionId;
  },

  async sendMessage(message) {
    if (CONFIG.USE_MOCK) {
      await new Promise((r) => setTimeout(r, 700 + Math.random() * 500)); // fake latency
      const hit = mockMatch(message);
      if (hit) return { reply: hit.answer, sources: [hit.source], error: null, session_id: sessionId };
      return { reply: ASSISTANT_IDENTITY.fallback, sources: [], error: null, session_id: sessionId };
    }

    // ---- Real backend call ----
    try {
      const headers = { "Content-Type": "application/json" };
      const apiKey = import.meta.env.VITE_API_KEY;
      if (apiKey) {
        headers["x-api-key"] = apiKey;
      }

      const res = await fetch(`${CONFIG.API_BASE_URL}/chat`, {
        method: "POST",
        headers,
        body: JSON.stringify({ message, session_id: sessionId }),
      });

      if (!res.ok) {
        let errorMessage = "Something went wrong. Please try again.";
        try {
          const payload = await res.json();
          if (payload?.error) errorMessage = payload.error;
        } catch {
          // Keep the generic fallback if the server did not return JSON.
        }
        return { reply: null, sources: [], error: errorMessage };
      }

      const data = await res.json();
      if (data?.session_id) {
        sessionId = data.session_id;
      }
      return {
        reply: data.reply,
        sources: data.sources || [],
        error: data.error || null,
        session_id: data.session_id || sessionId,
      };
    } catch (err) {
      return { reply: null, sources: [], error: "Couldn't reach the assistant. Please try again." };
    }
  },
};
