# SignalGraph AI

**Agentic RAG assistant for engineering operations** — connects incidents, logs and runbooks into source-cited operational memory.

> Upload your incident reports, runbooks and postmortems. Ask questions, investigate errors and find similar past incidents with full source citations.

---

## What is SignalGraph AI?

SignalGraph AI helps engineering teams answer operational questions:

- **Have we seen this issue before?**
- **What fixed it last time?**
- **Which service is affected?**
- **Which runbook is relevant?**
- **What evidence supports the answer?**

It combines **Retrieval-Augmented Generation (RAG)**, rule-based entity extraction, incident similarity search and a multi-step agentic investigation workflow — all without requiring external LLM API keys.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                │
│  WorkspaceList │ Upload │ Ask │ Investigate │ Dashboard │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP (REST)
┌───────────────────────▼─────────────────────────────────┐
│                 FastAPI Backend (Python 3.11)            │
│                                                         │
│  Ingestion ──► Chunking ──► Embeddings (sentence-trans) │
│  Entity Extraction (regex/rule-based)                   │
│  Retrieval (pgvector cosine similarity)                 │
│  Investigation (5-step agentic workflow)                │
│  Pattern Detection                                      │
│  MockLlmService (no API key required)                   │
└───────────────────────┬─────────────────────────────────┘
                        │ SQLAlchemy async
┌───────────────────────▼─────────────────────────────────┐
│              PostgreSQL + pgvector                       │
│  workspaces │ documents │ chunks │ entities │ relationships │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Docker and Docker Compose

### 1. Clone and start

```bash
git clone https://github.com/AbaSheger/SignalGraph-AI.git
cd SignalGraph-AI
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Seed sample data

```bash
# Create a workspace
WORKSPACE=$(curl -s -X POST http://localhost:8000/workspaces \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo Workspace"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Upload all sample files
for file in sample-data/*.md; do
  curl -s -X POST "http://localhost:8000/workspaces/$WORKSPACE/upload" -F "file=@$file"
  echo " -> uploaded $file"
done
```

### 3. Open the browser

Navigate to http://localhost:3000 and explore the workspace.

---

## Demo Flow

Using the included sample data (`sample-data/`):

### Step 1 — Create a workspace

Open http://localhost:3000, enter a name like `Ops Demo`, click **Create Workspace**.

### Step 2 — Upload sample data

Go to **Upload** and drag all 6 files from `sample-data/`:
- `payment-api-timeout.md` — incident report
- `auth-service-jwt-error.md` — incident report
- `kafka-consumer-lag.md` — incident report
- `database-connection-pool.md` — runbook
- `deployment-rollback-runbook.md` — runbook
- `incident-postmortem-001.md` — postmortem

### Step 3 — Ask a question

Go to **Ask**, type:
> *What caused the payment API timeout and how was it fixed?*

You will get a cited answer referencing the specific document with a confidence score.

### Step 4 — Investigate an error

Go to **Investigate**, paste:
> *ConnectionTimeout error in payment-api service, database pool exhausted*

The 5-step investigation will:
1. Classify the query as an incident
2. Find similar past incidents
3. Find relevant runbooks
4. Collect evidence citations
5. Generate a cited answer

### Step 5 — Find similar incidents

Go to **Similar Incidents**, paste any error message. Ranked similar incidents appear with service name, root cause, fix and runbook references.

### Step 6 — View patterns

Go to **Patterns** to see top affected services, recurring errors, incidents without root cause and services missing runbooks.

---

## API Reference

### Workspaces

#### `POST /workspaces`

```json
{ "name": "My Workspace", "description": "Optional" }
```

#### `GET /workspaces`

Returns a list of all workspaces.

---

### Documents

#### `POST /workspaces/{id}/upload`

Multipart form upload. Field name: `file`. Supported: `.md`, `.txt`, `.json`.

#### `GET /workspaces/{id}/sources`

All ingested documents.

#### `GET /workspaces/{id}/incidents`

Documents classified as incidents with extracted entity data (service, error type, severity, root cause, fix, runbook).

#### `GET /workspaces/{id}/runbooks`

Runbook documents.

#### `GET /workspaces/{id}/services`

Unique service names extracted from entities.

---

### Q&A and Investigation

#### `POST /workspaces/{id}/ask`

RAG question answering with citations.

**Request:**
```json
{ "query": "What caused the payment API timeout?" }
```

**Response:**
```json
{
  "answer": "Based on ingested documents...",
  "confidence": 0.8,
  "citations": [
    { "source": "payment-api-timeout.md", "chunk_index": 0, "score": 0.923, "excerpt": "..." }
  ],
  "missing_evidence": []
}
```

#### `POST /workspaces/{id}/investigate`

5-step agentic investigation.

**Request:**
```json
{ "query": "ConnectionTimeout in payment-api" }
```

**Response includes:** `query_type`, `steps`, `similar_incidents`, `relevant_runbooks`, `answer`, `confidence`, `citations`, `missing_evidence`.

#### `POST /workspaces/{id}/similar-incidents`

**Request:**
```json
{ "query": "DB connection pool exhausted" }
```

**Response:**
```json
{
  "results": [
    {
      "document_id": "...",
      "filename": "payment-api-timeout.md",
      "score": 0.91,
      "service_name": "payment-api",
      "root_cause": "connection pool exhaustion",
      "fix_or_workaround": "increase pool size",
      "related_runbook": "deployment-rollback-runbook.md",
      "excerpt": "..."
    }
  ]
}
```

---

### Dashboard

#### `GET /workspaces/{id}/patterns`

```json
{
  "top_services": [["payment-api", 2], ["auth-service", 1]],
  "recurring_errors": ["ConnectionTimeout", "JWTValidationError"],
  "reusable_fixes": ["increase pool size"],
  "incidents_without_root_cause": [],
  "services_missing_runbook": []
}
```

---

## Screenshots

> Add screenshots here after running the demo.

| Page | Description |
|---|---|
| Workspace List | Create and manage isolated workspaces |
| Upload | Drag-and-drop file ingestion |
| Ask | Free-text Q&A with cited answers |
| Investigate | 5-step agentic investigation workflow |
| Similar Incidents | Ranked similarity search |
| Service Graph | Visual service/incident/error map |
| Pattern Dashboard | Risk indicators and recurring patterns |
| Source Viewer | Browse all ingested documents |

---

## Configuration

### Backend Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DB_USER` | `sgadmin` | PostgreSQL username |
| `DB_PASSWORD` | `changeme` | PostgreSQL password |
| `DB_HOST` | `db` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `signalgraph` | Database name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | sentence-transformers model |
| `CHUNK_SIZE` | `512` | Words per chunk |
| `CHUNK_OVERLAP` | `64` | Word overlap between chunks |
| `MAX_CHUNKS_RETRIEVED` | `5` | Max chunks returned per query |
| `LLM_PROVIDER` | `mock` | LLM backend (`mock` in MVP) |

### LLM Provider Switching

The `LlmService` interface can be extended to add real providers:

```python
# backend/app/services/llm/openai.py
class OpenAILlmService(LlmService):
    def generate_answer(self, query, context_chunks, citations):
        # call OpenAI API
        ...
```

Set `LLM_PROVIDER=openai` and register in `backend/app/services/__init__.py`.

### Frontend Environment Variables

| Variable | Default | Description |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL |

---

## Running Tests

### Backend

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm install
npm test
```

---

## Project Structure

```
signalgraph-ai/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── app/
│       ├── main.py                  # FastAPI app entry point
│       ├── config.py                # Settings via pydantic-settings
│       ├── database.py              # Async SQLAlchemy engine
│       ├── models/                  # ORM table definitions
│       ├── schemas/                 # Pydantic schemas
│       ├── services/
│       │   ├── ingestion.py         # Parse → chunk → embed → store
│       │   ├── embedding.py         # sentence-transformers wrapper
│       │   ├── entity_extraction.py # Rule-based entity extraction
│       │   ├── retrieval.py         # pgvector similarity retrieval
│       │   ├── similarity.py        # Incident similarity search
│       │   ├── investigation.py     # 5-step agentic workflow
│       │   ├── pattern_detection.py # Pattern/risk analysis
│       │   └── llm/                 # LLM interface + MockLlmService
│       ├── routers/                 # FastAPI route handlers
│       └── utils/                   # Text parsing utilities
├── frontend/
│   ├── src/
│   │   ├── pages/                   # 8 UI pages
│   │   ├── components/              # Shared UI components
│   │   ├── api/client.ts            # Typed API client
│   │   ├── hooks/useWorkspace.ts
│   │   └── types/index.ts
│   └── tests/                       # Vitest component tests
└── sample-data/                     # 6 sample incident/runbook files
```

---

## Roadmap

- [ ] Real LLM providers (OpenAI, Anthropic, Ollama)
- [ ] Real knowledge graph (Neo4j or similar)
- [ ] Jira and GitHub integration
- [ ] Slack notifications
- [ ] OpenTelemetry trace ingestion
- [ ] Streaming investigation responses
- [ ] Multi-user auth (OAuth2/JWT)
- [ ] Automated ingestion from PagerDuty, OpsGenie
