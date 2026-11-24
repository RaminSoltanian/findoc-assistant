# FinDoc Assistant

An AI assistant that answers questions about Canadian banking and mortgage documents, built step by step toward a production-style system: answers with citations, AI agents, evaluations, guardrails and cloud deployment.

> **Status:** Milestone 1 of 12, LLM API service (in progress)

---

## What it does today (Milestone 1)

- A FastAPI service with an `/ask` endpoint
- Sends the question to an AI model (Azure OpenAI via Microsoft Foundry)
- Always returns the answer in the same fixed JSON format, validated with Pydantic
- Politely declines questions that are not about banking or mortgages
- A **golden set** of 20 test questions with known correct answers, used to measure quality in every later milestone

At this stage the assistant answers from the model's general knowledge only. Answering from documents, with citations, starts in Milestone 2.

---

## Example

**Request**

```http
POST /ask
Content-Type: application/json

{ "question": "What does CMHC stand for?" }
```

**Response**

```json
{
  "answer": "Canada Mortgage and Housing Corporation, the federal housing agency that also provides mortgage default insurance.",
  "confidence": "high",
  "topic": "mortgage",
  "needs_source_document": false
}
```

**Off-topic question**

```json
{
  "answer": "Sorry, I can only help with banking and mortgage questions.",
  "confidence": "high",
  "topic": "out_of_scope",
  "needs_source_document": false
}
```

---

## Getting started

### Prerequisites

- Python 3.12+
- Docker Desktop
- An AI model deployment, e.g. a chat model deployed in Microsoft Foundry (Azure OpenAI)

### 1. Configure

Copy the example settings and fill in your own values:

```bash
cp .env.example .env
```

```env
LLM_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1/
LLM_API_KEY=<your-key>
LLM_MODEL=<your-deployment-name>
```

`.env` is in `.gitignore`. Never commit real keys.

### 2. Run with Docker

```bash
docker compose up --build
```

This starts the API on `http://localhost:8000` and a PostgreSQL + pgvector database (used from Milestone 2).

Open `http://localhost:8000/docs` to try `/ask` in the browser.

### 3. Or run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Run the tests

```bash
pytest
```

Tests replace the real model with a fake one, so they are fast and free. GitHub Actions runs them on every push.

---

## Project structure

```
app/
  main.py        API endpoints (/ask, /health)
  llm.py         the only place that calls the AI model
  schemas.py     request and answer formats (Pydantic)
  prompts.py     system prompt and few-shot examples
  config.py      settings loaded from .env
data/raw/        public source documents (Milestone 2+)
evals/
  golden_set.jsonl   test questions with expected answers and sources
  run_baseline.py    runs the golden set against the API
tests/           automated tests
.github/workflows/   CI pipeline
```

---

## Evaluation

| Version | Golden set score | Notes |
|---|---|---|
| M1: model only, no documents | 12 / 20 | Baseline |

Each milestone adds a row, so improvements are measured rather than claimed.

---

## Roadmap

| # | Milestone | Status |
|---|---|---|
| M1 | LLM API service: structured answers, golden set | In progress |
| M2 | Document Q&A: answers from PDFs with citations | Planned |
| M3 | Better search: hybrid search, reranking, per-user permissions | Planned |
| M4 | Quality gate: evals in CI, tracing and cost tracking | Planned |
| M5 | Single agent: tool calling, read-only SQL, human approval | Planned |
| M6 | MCP tool server | Planned |
| M7 | Multi-agent team: supervisor + specialists | Planned |
| M8 | Guardrails and LLM gateway: injection tests, provider fallback | Planned |
| M9 | Azure deployment with Entra ID sign-in | Planned |
| M10 | .NET agent with Microsoft Agent Framework on Microsoft Foundry | Planned |
| M11 | Governance pack: model card and validation report | Planned |
| M12 | Portfolio and demo | Planned |

---

## Data

This project uses only **public documents** (e.g. OSFI guidelines, CMHC and FCAC mortgage guides, bank annual reports) and **synthetic data**. No real customer or employer data is used.

---

## Tech stack

Python · FastAPI · Pydantic · OpenAI SDK (Azure OpenAI via Microsoft Foundry) · PostgreSQL + pgvector · Docker · GitHub Actions · pytest

---

## License

MIT
