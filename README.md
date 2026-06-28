# Base LLM Agent

A lightweight, extensible Python LLM agent built to run effortlessly on an M3 MacBook Pro (16GB RAM). It features `uv` for ultra-fast dependency management and allows seamless hot-swapping between local models and cloud APIs.

## Prerequisites

1. **Python 3.11+**
2. **uv** (Install via `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`)
3. **Ollama** (For running local models. [Download here](https://ollama.com))

---

## Setup & Local Execution

### 1. Clone & Environment Setup

Copy the example environment file and fill in your keys if using cloud models:

```bash
cp .env.example .env
```

### Local Execution

1. Ensure your .env contains:

```bash
MODEL_PROVIDER=local
LOCAL_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434/v1
```

2. Start the local LLM engine:

```bash
ollama run llama3
```

3. Execute the agent:

```bash
uv run src/agent.py
```
