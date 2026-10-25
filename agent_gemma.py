"""
GemmaBrowserAgent - agent_gemma.py
===================================
Hackathon demo: Launch a browser-use Agent powered by ChatBrowserUse —
the fastest and most accurate model for browser automation tasks.

Usage:
    python agent_gemma.py

Requirements (.env):
    BROWSER_USE_API_KEY=your-browser-use-api-key
    TASK="Your browser task here"      # optional, has a default
"""

import asyncio
import os

from dotenv import load_dotenv

from browser_use import Agent, ChatBrowserUse

load_dotenv()

# ---------------------------------------------------------------------------
# ChatBrowserUse is the recommended model for browser automation:
# - Highest accuracy + fastest speed + lowest token cost
# - Built specifically for the Browser Use library
# Get your API key at: https://cloud.browser-use.com/new-api-key
# ---------------------------------------------------------------------------
API_KEY: str | None = os.getenv("BROWSER_USE_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "No Browser Use API key found. "
        "Set BROWSER_USE_API_KEY in your .env file. "
        "Get one free at https://cloud.browser-use.com/new-api-key"
    )

DEFAULT_TASK = (
    "Go to https://github.com/trending/python and list the top-5 "
    "trending Python repositories today with their star counts and a "
    "one-sentence description."
)


async def main() -> None:
    """Run the browser agent with ChatBrowserUse."""
    task = os.getenv("TASK", DEFAULT_TASK)
    llm = ChatBrowserUse()

    print(f"\n GemmaBrowserAgent starting ...")
    print(f"   Model : ChatBrowserUse")
    print(f"   Task  : {task}\n")

    agent = Agent(task=task, llm=llm)
    result = await agent.run()

    print("\n Task complete!")
    print("=" * 60)
    print(result.final_result())
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

