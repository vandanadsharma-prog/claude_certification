# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A learning/experimentation project for the Anthropic Claude API. All code lives in Jupyter notebooks under `practice_notebooks/`. There are no `.py` source files or automated tests.

## Setup

Install dependencies (run once in a notebook cell or terminal):
```bash
pip install python-dotenv anthropic
```

Set `ANTHROPIC_API_KEY` in a `.env` file at the project root (already gitignored).

## Running the Notebooks

```bash
# Launch Jupyter
jupyter notebook practice_notebooks/

# Or open a specific notebook
jupyter notebook practice_notebooks/chat-notebook.ipynb
jupyter notebook practice_notebooks/eval-workflow.ipynb
```

Run cells sequentially top-to-bottom. The interactive chat loop in `chat-notebook.ipynb` exits when the user types `"exit"`.

## Architecture

### chat-notebook.ipynb
Multi-turn chatbot with two modes:
- `chat()` — standard blocking API call, prints full response
- `chat_stream()` — streaming API call, prints tokens as they arrive

Both functions share a `messages` list for conversation history via `append_message()`. Model defaults to `claude-sonnet-4-6`, temperature `0.1`.

### eval-workflow.ipynb
Two-stage LLM pipeline using `claude-haiku-4-5`:
1. **Dataset generation** — prompts the model to produce 3 evaluation tasks (factuality, date reasoning, multi-hop reasoning) and writes them to `dataset.json`
2. **Grading** — a separate grader function scores model responses 1–5 against the task's `solution_criteria`, returning a JSON verdict (PASS if score ≥ 4)

`dataset.json` is the artifact produced by the generation stage and consumed by the grading stage.

## Key Patterns

- All API clients are initialized with `anthropic.Anthropic()`, which auto-reads `ANTHROPIC_API_KEY` from the environment via `python-dotenv`.
- Streaming uses the `client.messages.stream()` context manager; non-streaming uses `client.messages.create()`.
- Model responses expected as JSON are extracted with `json.loads(response.content[0].text)`.
