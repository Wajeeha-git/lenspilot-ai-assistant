// ============================================================
// MEMBER 2 — KNOWLEDGE / PROMPT OWNER
// ============================================================
// Edit this file only. Plain JS objects — no React knowledge needed.
// Keep the key names (keywords, answer, source) the same so the
// widget code keeps working.

export const ASSISTANT_IDENTITY = {
  name: "LensPilot AI Assistant",
  greeting: "Hi there! 👋 How can I help you today?",
  fallback:
    "I don't have that in my docs yet, so I don't want to guess. Could you rephrase, or ask about pricing, features, or getting started?",
};

// Quick-reply chips shown under the greeting.
export const SUGGESTED_QUESTIONS = [
  "What is this platform about?",
  "How does it work?",
  "Is it free to try?",
];

// Mock knowledge base — keyword-matched to fake a real RAG answer
// while there's no backend yet. `source` mirrors the "sources" field
// the real /chat response will send once Member 1's endpoint is live.
export const KNOWLEDGE_BASE = [
  {
    keywords: ["what is", "about", "platform", "lenspilot"],
    answer:
      "LensPilot helps you build and embed AI-powered chat experiences seamlessly into your website or app. It's fast, secure, and easy to use.",
    source: "product-overview.md",
  },
  {
    keywords: ["how does it work", "how it works", "work"],
    answer:
      "You connect your docs, LensPilot indexes them, and the widget answers visitor questions using only that content — with sources attached to every answer.",
    source: "how-it-works.md",
  },
  {
    keywords: ["free", "trial", "pricing", "cost", "price"],
    answer:
      "Yes — there's a free trial with no credit card required. Paid plans unlock higher usage limits and custom branding.",
    source: "pricing.md",
  },
  {
    keywords: ["secure", "privacy", "data", "encrypt"],
    answer:
      "Your data is encrypted in transit and at rest, and it's never used to train shared models.",
    source: "security-faq.md",
  },
  {
    keywords: ["integrate", "embed", "install", "script"],
    answer:
      "Add one script tag to your site and the widget appears automatically — no framework required.",
    source: "integration-guide.md",
  },
];
