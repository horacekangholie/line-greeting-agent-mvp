from __future__ import annotations

from dotenv import load_dotenv
import gradio as gr

from src.line_greeter.config import get_settings
from src.line_greeter.openai_agent import GreetingAgent
from src.line_greeter.line_client import LineClient


load_dotenv(override=False)

agent = GreetingAgent()
line = LineClient()

import os

print("DEBUG OPENAI_API_KEY exists?", bool(os.getenv("OPENAI_API_KEY")))
print("DEBUG OPENAI_API_KEY prefix:", (os.getenv("OPENAI_API_KEY") or "")[:7])
print("DEBUG OPENAI_MODEL:", os.getenv("OPENAI_MODEL"))


def generate_greeting(style: str, user_context: str) -> str:
    return agent.generate(style=style, user_context=user_context)


def send_greeting(style: str, user_context: str) -> str:
    s = get_settings()
    s.validate_or_raise()
    msg = agent.generate(style=style, user_context=user_context)
    line.push_text(user_id=s.line_user_id, text=msg)
    return f"✅ Sent to LINE userId={s.line_user_id}\n\nMessage:\n{msg}"


with gr.Blocks(title="LINE Greeting Agent MVP") as demo:
    gr.Markdown("# LINE Greeting Agent MVP\nGenerate & push a greeting to a LINE user.")

    style = gr.Dropdown(
        choices=["warm", "professional", "cheerful", "minimal"],
        value="warm",
        label="Greeting style",
    )
    user_context = gr.Textbox(
        label="Optional context (e.g., 'User likes hiking; keep it motivational')",
        lines=3,
    )

    out = gr.Textbox(label="Output", lines=6)

    with gr.Row():
        btn_gen = gr.Button("Generate (Preview)")
        btn_send = gr.Button("Generate + Send to LINE")

    btn_gen.click(generate_greeting, inputs=[style, user_context], outputs=[out])
    btn_send.click(send_greeting, inputs=[style, user_context], outputs=[out])

demo.launch()