# line-greeting-agent-mvp

## 📦 Overview

**line-greeting-agent-mvp** is a Minimal Viable Product (MVP) AI agent
that integrates the LINE Messaging API with an LLM-powered greeting
workflow.\
It listens to incoming LINE messages via webhook, processes them through
an agent controller, generates contextual greetings using an LLM, and
replies in real time.

This project demonstrates the fundamentals of **Agentic AI** in a
production-style, event-driven architecture.

------------------------------------------------------------------------

## 🚀 Features

-   🤖 LLM-powered greeting responses
-   💬 LINE Messaging API webhook integration
-   🔁 Event-driven agent loop (input → reasoning → response)
-   ⚡ Lightweight FastAPI-based backend
-   🧠 Prompt-based response generation
-   🧩 Extensible architecture for future multi-tool agents

------------------------------------------------------------------------

## 🧱 Architecture

    LINE User → LINE Webhook → FastAPI Server
                             ↓
                      Agent Controller
                             ↓
                      LLM Greeting Logic
                             ↓
                       Response Formatter
                             ↓
                     Reply via LINE API

This follows a simplified **Agentic Workflow**: \> Input → Reasoning
(LLM) → Action → Output

------------------------------------------------------------------------

## 🎯 Purpose

This MVP serves as: - A foundational hands-on implementation of Agentic
AI - A portfolio-ready demo of real-time AI agent deployment - A
stepping stone toward multi-agent orchestration systems - A baseline for
adding tools, memory, and planning loops

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python
-   FastAPI
-   LINE Messaging API
-   OpenAI / LLM API
-   Async event handling
-   dotenv for environment configuration

------------------------------------------------------------------------

## 📂 Project Structure

    line-greeting-agent-mvp/
    │
    ├── app/
    │   ├── main.py              # FastAPI entry point
    │   ├── agent.py             # Agent controller logic
    │   ├── llm.py               # LLM interaction layer
    │   └── line_handler.py      # LINE webhook processing
    │
    ├── .env.example             # Environment variable template
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## ⚙️ Setup

### 1. Clone the Repository

``` bash
git clone https://github.com/your-username/line-greeting-agent-mvp.git
cd line-greeting-agent-mvp
```

### 2. Create Virtual Environment

``` bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`:

    LINE_CHANNEL_SECRET=your_secret
    LINE_CHANNEL_ACCESS_TOKEN=your_token
    OPENAI_API_KEY=your_openai_key

### 5. Run the Server

``` bash
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## 🧠 Learning Outcomes

This project demonstrates: - Building real-time AI agents with
webhooks - Integrating LLM reasoning into production pipelines -
Designing extensible agent-controller architecture - Applying async
event-driven patterns for responsiveness

------------------------------------------------------------------------

## 🔮 Future Enhancements

-   Tool calling (calendar, weather, knowledge base)
-   Memory module with embeddings
-   Multi-agent collaboration workflows
-   RAG-powered contextual greetings
-   Cloud deployment with scalable webhook handling

------------------------------------------------------------------------

```bash
#### Test Run
````bash
uv run uvicorn src.line_greeter.capture_userid:app --host 0.0.0.0 --port 8000

ngrok http 8000
````

#### Test by pass calling LINE
````bash
curl -Method POST "https://comfortingly-tendrilly-sarina.ngrok-free.dev/line/webhook" -Headers @{ "Content-Type" = "application/json" } -Body '{"events":[{"source":{"userId":"Utest"},"message":{"type":"text","text":"hello"}}]}'
````

```