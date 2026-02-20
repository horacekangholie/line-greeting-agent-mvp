from __future__ import annotations

import os
from dotenv import load_dotenv

from line_greeter.config import settings
from line_greeter.openai_agent import GreetingAgent
from line_greeter.line_client import LineClient


def main() -> None:
    # Loads .env locally. On Hugging Face, env vars come from Space/Job secrets.
    load_dotenv(override=False)

    settings.validate_or_raise()

    agent = GreetingAgent()
    line = LineClient()

    style = os.getenv("GREETING_STYLE", settings.greeting_style)
    user_context = os.getenv("USER_CONTEXT", "").strip()

    msg = agent.generate(style=style, user_context=user_context)
    line.push_text(user_id=settings.line_user_id, text=msg)

    print("✅ Sent greeting to LINE user.")


if __name__ == "__main__":
    main()