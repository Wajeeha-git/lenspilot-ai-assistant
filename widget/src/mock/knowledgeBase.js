export const ASSISTANT_IDENTITY = {
  name: "LensPilot AI Assistant",
  greeting: "Hi there. How can I help you today?",
  fallback: "I'm not certain about that. Please contact the LensPilot support team.",
};

export const SUGGESTED_QUESTIONS = [
  "What is LensPilot?",
  "How does LensPilot work?",
  "Do customers need an app?",
];

export const KNOWLEDGE_BASE = [
  {
    keywords: ["what is", "about", "platform", "lenspilot"],
    answer:
      "LensPilot is an AI-powered browser-based platform that lets customers virtually try on contact lenses using real-time iris segmentation and augmented reality.",
    source: "product-overview.md",
  },
  {
    keywords: ["how does it work", "how it works", "work"],
    answer:
      "A customer scans a shopkeeper's QR code, opens LensPilot in the browser, allows camera access, and sees contact lens colors overlaid on their eyes in real time.",
    source: "workflow.md",
  },
  {
    keywords: ["app", "install", "download"],
    answer:
      "No. LensPilot is browser-based, so customers can use the try-on experience without installing an app.",
    source: "faq-general.md",
  },
  {
    keywords: ["camera", "permission", "access"],
    answer:
      "LensPilot needs camera access so the AI can detect the iris and place the lens overlay in real time.",
    source: "faq-technical.md",
  },
  {
    keywords: ["shopkeeper", "retailer", "qr"],
    answer:
      "Shopkeepers register, subscribe to a plan, and receive a unique QR code that customers scan to start the virtual try-on.",
    source: "workflow.md",
  },
];
