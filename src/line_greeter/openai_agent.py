from __future__ import annotations

from typing import Iterable, Optional

from openai import OpenAI

from .config import get_settings
from .history_store import ChatTurn


class GreetingAgent:
    """
    Two capabilities:
    - generate(): one-off greeting text (used by app.py push feature)
    - reply(): conversational reply that uses recent history
    """

    def __init__(self) -> None:
        s = get_settings()
        self.client = OpenAI(api_key=s.openai_api_key)
        self.model = s.openai_model

    def generate(self, style: str, user_context: str = "") -> str:
        style = (style or "warm").strip()
        user_context = (user_context or "").strip()

        instructions = (
            "You write short, friendly greeting messages for LINE chat.\n"
            "Rules:\n"
            "- Keep it under 2 short sentences.\n"
            "- No emojis unless user explicitly asks.\n"
            "- Sound natural and warm.\n"
        )

        prompt = f"Style: {style}\n"
        if user_context:
            prompt += f"Context: {user_context}\n"
        prompt += "Write today's greeting."

        resp = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=prompt,
        )
        text = (resp.output_text or "").strip()
        return text or "Hello! Hope you have a great day today."

    def reply(self, user_text: str, history: Optional[Iterable[ChatTurn]] = None) -> str:
        """
        Produce a reply using recent turns (per-user).
        Keeps the response short because it's LINE chat.
        """
        user_text = (user_text or "").strip()

        instructions = (
            "You are a helpful LINE chat assistant.\n"
            "Rules:\n"
            "- Reply in 1-3 short sentences.\n"
            "- Be natural and friendly.\n"
            "- Use the conversation history to stay consistent.\n"
            "- If the user asks you to remember something, you may acknowledge it.\n"
            "- Do NOT invent personal facts.\n"
        )

        # Format history as a plain transcript (MVP approach)
        hist_lines = []
        if history:
            for t in history:
                prefix = "User" if t.role == "user" else "Assistant"
                hist_lines.append(f"{prefix}: {t.text}")
        hist_block = "\n".join(hist_lines[-30:])  # hard cap

        prompt = (
            "Conversation so far:\n"
            f"{hist_block}\n\n"
            f"User: {user_text}\n"
            "Assistant:"
        )

        resp = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=prompt,
        )
        text = (resp.output_text or "").strip()
        return text or "Got it!"