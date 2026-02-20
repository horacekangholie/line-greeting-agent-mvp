from __future__ import annotations
import requests
from .config import get_settings


class LineClient:
    def push_text(self, user_id: str, text: str) -> None:
        s = get_settings()
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {s.line_channel_access_token}",
            "Content-Type": "application/json",
        }
        payload = {"to": user_id, "messages": [{"type": "text", "text": text}]}
        print("DEBUG LINE to =", repr(user_id), "len=", len(user_id))
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code >= 400:
            raise RuntimeError(f"LINE push failed ({r.status_code}): {r.text}")