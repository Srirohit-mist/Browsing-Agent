"""
GemmaBrowserAgent - agent_gemma.py
===================================
Hackathon demo: Launch a browser-use Agent using Gemma 4 / Gemini API
with multimodal capabilities (text + DOM screenshots).

Usage:
    uv run agent_gemma.py

Requirements (.env):
    GEMINI_API_KEY=your-google-ai-studio-key
    TASK="Your browser task here"      # optional, has a default
"""

import asyncio
import os

from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm.google import ChatGoogle

load_dotenv()

# ---------------------------------------------------------------------------
# Model selection
# Gemma 4 is accessed through the Gemini API with model ID "gemma-3-27b-it".
# Swap to any VerifiedGeminiModels string as needed:
#   "gemini-3.8-flash"   -> fast, multimodal (recommended)
#   "gemini-2.5-pro"     -> most capable
#   "gemma-3-27b-it"     -> open-weight Gemma via Gemini API
# ---------------------------------------------------------------------------
MODEL_ID: str = os.getenv("GEMMA_MODEL", "gemini-3.8-flash")
API_KEY: str | None = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "No Gemini API key found. "
        "Set GEMINI_API_KEY in your .env file. "
        "Get one free at https://aistudio.google.com/app/apikey"
    )

DEFAULT_TASK = (
    "Go to https://github.com/trending/python and list the top-5 "
    "trending Python repositories today with their star counts and a "
    "one-sentence description."
)


def build_llm() -> ChatGoogle:
    """Construct a ChatGoogle LLM wired to the Gemma/Gemini model."""
    return ChatGoogle(
        model=MODEL_ID,
        api_key=API_KEY,
        temperature=0.3,
        max_output_tokens=4096,
    )


async def main() -> None:
    task = os.getenv("TASK", DEFAULT_TASK)
    llm = build_llm()

    print(f"\n GemmaBrowserAgent starting ...")
    print(f"   Model : {MODEL_ID}")
    print(f"   Task  : {task}\n")

    agent = Agent(task=task, llm=llm)
    result = await agent.run()

    print("\n Task complete!")
    print("=" * 60)
    print(str(result).encode('utf-8', errors='replace').decode('utf-8'))
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
