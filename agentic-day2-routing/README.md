# Agentic Day 2 — Routing

A LangChain + Claude project demonstrating **agentic routing**: classifying user queries and dispatching them to the appropriate specialized handler.

## Overview

The router inspects each incoming message and directs it to one of three agents:

| Route | Handles |
|-------|---------|
| `math` | Arithmetic, algebra, and numerical reasoning |
| `code` | Programming questions, debugging, and code generation |
| `general` | Everything else — facts, summaries, open-ended questions |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
python app.py
```

Enter queries at the prompt. Type `quit` to exit.

## Project Structure

```
├── app.py           # Main router + agent loop
├── requirements.txt
├── .gitignore
└── README.md
```
