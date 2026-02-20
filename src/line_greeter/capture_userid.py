from __future__ import annotations

from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import requests

# import your agent
from .openai_agent import GreetingAgent

load_dotenv()
app = FastAPI()

agent = GreetingAgent()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()


@app.get("/")
def health():
    return {"ok": True}


@app.post("/line/webhook")
async def webhook(req: Request):
    payload = await req.json()

    for event in payload.get("events", []):
        if event.get("type") != "message":
            continue

        message = event.get("message", {})
        if message.get("type") != "text":
            continue

        user_text = message.get("text", "")
        reply_token = event.get("replyToken")

        # Generate AI reply
        ai_reply = agent.generate(style="warm", user_context=user_text)

        # Send reply via LINE Reply API
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        body = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": ai_reply}],
        }

        requests.post(url, headers=headers, json=body, timeout=10)

    return {"ok": True}