<!-- GemmaBrowserAgent -->
<div align="center">

# 🦾 GemmaBrowserAgent

### *Open-weight AI meets the open web — autonomous browser automation powered by Gemma & the Gemini API*

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built on browser-use](https://img.shields.io/badge/built%20on-browser--use-8B5CF6)](https://github.com/browser-use/browser-use)

**Forked from [browser-use](https://github.com/browser-use/browser-use) for the Google Gemma Hackathon 2026.**

</div>

---

## What is GemmaBrowserAgent?

GemmaBrowserAgent is a hackathon fork of the open-source `browser-use` project that wires **Google's Gemma / Gemini models** directly into a full browser-automation agent. It lets an open-weight LLM see, reason about, and act on any website — using screenshots and DOM snapshots together for true multimodal understanding.

Two ready-to-run scripts are included:

| Script | Purpose |
|--------|---------|
| `agent_gemma.py` | General-purpose Gemma-powered browser agent |
| `doc_scraper.py` | Specialised documentation scraper that outputs a structured Markdown summary |

---

## ✨ Key Features

- **Gemma 4 / Gemini API integration** — plug in `gemma-3-27b-it`, `gemini-2.5-flash`, `gemini-2.5-pro`, or any other Google model with one env var
- **Multimodal** — the agent processes text *and* DOM screenshots in a single context window
- **Documentation Scraper** — crawl any docs site and get back a clean, structured Markdown summary
- **uv-first workflow** — single-command setup, no virtualenv juggling
- **All browser-use features** — stealth, CAPTCHA handling, parallel tabs, and more

---

## 🚀 Quick-Start (5 minutes)

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A free [Gemini API key](https://aistudio.google.com/app/apikey)

### 2. Clone & install

```bash
git clone https://github.com/<your-username>/GemmaBrowserAgent.git
cd GemmaBrowserAgent

# create a uv project and install dependencies
uv init --python 3.12
uv add browser-use python-dotenv
uv run playwright install chromium
```

### 3. Configure

```bash
cp .env.example .env
# Open .env and set GEMINI_API_KEY=<your key>
```

### 4. Run the general agent

```bash
uv run agent_gemma.py
```

Override the task inline:

```bash
TASK="Find the latest release notes for Python 3.14" uv run agent_gemma.py
```

### 5. Run the documentation scraper

```bash
uv run doc_scraper.py
```

Scrape a different site (saves Markdown to `./output/`):

```bash
DOC_URL=https://docs.pydantic.dev MAX_PAGES=8 uv run doc_scraper.py
```

---

## ⚙️ Configuration Reference

All config lives in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | *(required)* | Your Google AI Studio API key |
| `GEMMA_MODEL` | `gemma-3-27b-it` | Model ID — any Gemini/Gemma model string |
| `TASK` | See `agent_gemma.py` | Override the default agent task |
| `DOC_URL` | `https://docs.browser-use.com` | Target docs site for the scraper |
| `MAX_PAGES` | `5` | Max pages to crawl in the scraper |
| `OUTPUT_DIR` | `./output` | Where scraped Markdown files are saved |
| `BROWSER_USE_LOGGING_LEVEL` | `info` | Logging verbosity (`debug`/`info`/`warning`) |
| `ANONYMIZED_TELEMETRY` | `false` | Opt out of telemetry |

---

## 🧠 How It Works

```
User Task  ──►  GemmaBrowserAgent
                      │
              ┌───────▼────────┐
              │  browser-use   │  ← orchestration, tool execution
              │  Agent loop    │
              └───────┬────────┘
                      │  screenshot + DOM snapshot
              ┌───────▼────────┐
              │  ChatGoogle    │  ← Gemma/Gemini via google-genai SDK
              │  (multimodal)  │
              └───────┬────────┘
                      │  next action (click / type / navigate / done)
              ┌───────▼────────┐
              │   Playwright   │  ← real Chromium browser
              └────────────────┘
```

The agent loop:
1. Takes a screenshot + extracts the DOM
2. Sends both to Gemma/Gemini along with the task and history
3. Gemma returns the next browser action
4. Playwright executes it
5. Repeat until the task is complete

---

## 📂 Project Structure

```
GemmaBrowserAgent/
├── agent_gemma.py       # ← NEW: General Gemma agent entry point
├── doc_scraper.py       # ← NEW: Documentation scraper agent
├── .env.example         # ← NEW: Env template with Gemini config
├── output/              # ← scraped summaries land here
│
├── browser_use/         # Core browser-use library (upstream)
│   ├── llm/google/      # ChatGoogle wrapper (supports all Gemma/Gemini models)
│   ├── agent/           # Agent loop, prompts, memory
│   └── browser/         # Playwright session management
│
└── examples/            # Upstream example scripts
```

---

## 🎯 Hackathon Requirements Mapping

| Requirement | Implementation |
|-------------|---------------|
| **AI Integration (Gemma 4 / Gemini API)** | `agent_gemma.py` — uses `ChatGoogle(model="gemma-3-27b-it")` via `google-genai` SDK |
| **Multimodal (text + images)** | `ChatGoogle` sends DOM snapshots + screenshots to the model each step |
| **Custom use case** | `doc_scraper.py` — crawls docs sites and outputs structured Markdown summaries |
| **Unique branding** | This README + project name `GemmaBrowserAgent` |
| **uv setup** | Single `uv add browser-use` install, `uv run` to execute |

---

## 🛠 Extending the Agent

### Use a different Gemini model

```python
# In agent_gemma.py or doc_scraper.py
llm = ChatGoogle(
    model="gemini-2.5-pro",   # or "gemini-2.5-flash", "gemma-3-27b-it"
    api_key=API_KEY,
    temperature=0.1,
)
```

### Add custom browser actions

```python
from browser_use.controller import Controller
from pydantic import BaseModel

controller = Controller()

@controller.action("Save page content to file")
def save_to_file(content: str, filename: str) -> str:
    with open(filename, "w") as f:
        f.write(content)
    return f"Saved to {filename}"

agent = Agent(task=task, llm=llm, controller=controller)
```

---

## 📜 License

MIT — see [LICENSE](LICENSE). This project is a fork of [browser-use](https://github.com/browser-use/browser-use), which is also MIT licensed.

---

<div align="center">

Built with ❤️ for the **Google Gemma Hackathon 2026**

[browser-use](https://github.com/browser-use/browser-use) · [Gemini API](https://aistudio.google.com/) · [google-genai SDK](https://github.com/googleapis/python-genai)

</div>
