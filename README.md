# LensPilot AI Assistant

> Intelligent AI-powered assistant for LensPilot — bridging smart conversations with actionable insights.

---

## 📋 Overview

LensPilot AI Assistant is a modular, API-driven chatbot system designed to power intelligent customer interactions. It combines a robust backend engine with an embeddable frontend widget, enabling seamless integration into any web application.

## 🏗️ Repository Structure

```
lenspilot-ai-assistant/
├── backend/          # API server, chat engine, ingestion pipeline
├── widget/           # Embeddable chat widget (frontend)
├── demo-site/        # Demo/testing site for the widget
├── docs/             # API contracts, architecture, guides
├── data/             # Knowledge base files, seed data
├── .env.example      # Environment variable template
├── .gitignore        # Git ignore rules
├── CONTRIBUTING.md   # Team workflow & contribution rules
└── CODEOWNERS        # File ownership assignments
```

## 🚀 Getting Started

### Prerequisites

- Node.js >= 18
- Python >= 3.10
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-org>/lenspilot-ai-assistant.git
   cd lenspilot-ai-assistant
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Follow the setup instructions in `backend/` and `widget/` READMEs.

## 📖 Documentation

- [API Contract](docs/API.md) — Request/response specs for all endpoints
- [Contributing Guide](CONTRIBUTING.md) — Branch naming, PR rules, team workflow

## 🔒 Branch Protection

The `main` branch is protected:
- All changes require a Pull Request
- At least 1 review approval is required
- Direct pushes and force pushes are blocked
- Status checks must pass before merging

## 📄 License

This is a private repository. All rights reserved.
