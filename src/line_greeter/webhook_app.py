from __future__ import annotations

from pathlib import Path
import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from .openai_agent import GreetingAgent
from .history_store import HistoryStore

# Ensure .env loads regardless of where uvicorn is launched from
ROOT = Path(__file__).resolve().parents[2]  # project root (line-greeting-agent-mvp/)
load_dotenv(ROOT / ".env", override=False)

app = FastAPI()
agent = GreetingAgent()

# Anchor DB path to project root so it doesn't end up in a random cwd
default_db_url = f"sqlite:///{(ROOT / 'chat_history.db').as_posix()}"
store = HistoryStore(db_url=os.getenv("CHAT_DB_URL", default_db_url))

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()


@app.get("/")
def health():
    return {"ok": True}


@app.post("/line/webhook")
async def line_webhook(req: Request):
    """
    LINE -> your webhook
    - store user message
    - load last N
    - call OpenAI
    - store assistant message
    - reply using Reply API (replyToken)
    """
    payload = await req.json()

    for event in payload.get("events", []):
        if event.get("type") != "message":
            continue

        message = event.get("message", {}) or {}
        if message.get("type") != "text":
            continue

        user_text = (message.get("text") or "").strip()
        reply_token = event.get("replyToken")
        user_id = (event.get("source", {}) or {}).get("userId")

        if not reply_token or not user_id:
            continue

        # Commands
        if user_text.lower() in ("/reset", "reset"):
            store.clear(user_id)
            ai_reply = "✅ Cleared our chat history."
            store.add(user_id=user_id, role="assistant", text=ai_reply)
        else:
            # 1) store user msg
            store.add(user_id=user_id, role="user", text=user_text)

            # 2) get recent history (including this msg)
            history = store.last_n(user_id=user_id, n=20)

            # 3) call OpenAI
            try:
                ai_reply = agent.reply(user_text=user_text, history=history)
            except Exception as e:
                print("OpenAI error:", repr(e))
                ai_reply = "I got your message! (Temporary fallback)"

            # 4) store assistant msg
            store.add(user_id=user_id, role="assistant", text=ai_reply)

        # 5) Reply API
        if not LINE_CHANNEL_ACCESS_TOKEN:
            print("Reply failed: missing LINE_CHANNEL_ACCESS_TOKEN")
            return {"ok": True}

        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        body = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": ai_reply}],
        }

        try:
            r = requests.post(url, headers=headers, json=body, timeout=10)
            if r.status_code >= 400:
                print(f"Reply failed for {user_id}: {r.status_code} {r.text}")
        except Exception as e:
            print("Reply request error:", repr(e))

    return {"ok": True}