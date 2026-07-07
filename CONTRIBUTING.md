# Contributing to SignalGraph AI

Thank you for your interest in contributing! SignalGraph AI is an open-source agentic RAG assistant for engineering operations. Every contribution — big or small — is welcome. 🎉

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Local Development Setup](#local-development-setup)
- [Project Structure](#project-structure)
- [Finding an Issue to Work On](#finding-an-issue-to-work-on)
- [Making a Contribution](#making-a-contribution)
- [Coding Guidelines](#coding-guidelines)
- [Running Tests](#running-tests)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Getting Help](#getting-help)

---

## Code of Conduct

Be kind, inclusive, and constructive. We welcome contributors of all experience levels. If you are new to open source — this is a great place to start!

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

| Tool | Version | Install |
|---|---|---|
| Git | any | https://git-scm.com |
| Docker | 24+ | https://docs.docker.com/get-docker/ |
| Docker Compose | v2+ | included with Docker Desktop |
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org |

> 💡 **New to Docker?** You only need it to run the full stack. For most backend issues (especially `good first issue` ones) you can work with just Python.

---

## Local Development Setup

### 1. Fork and clone the repo

```bash
# Fork via the GitHub UI, then:
git clone https://github.com/<your-username>/SignalGraph-AI.git
cd SignalGraph-AI
```

### 2. Start the full stack with Docker Compose

```bash
docker compose up --build
```

This starts:
- **Backend** (FastAPI) at http://localhost:8000
- **Frontend** (React + Vite) at http://localhost:5173
- **PostgreSQL** with pgvector at `localhost:5432`

### 3. Check the API is running

Open http://localhost:8000/docs — you'll see the Swagger UI with all available endpoints.

### 4. Seed sample data (optional but recommended)

```bash
# Upload all sample files to a test workspace
cd sample-data
# Create a workspace first via POST /workspaces in Swagger UI
# Then upload each .md file via POST /workspaces/{id}/upload
```

### 5. Backend-only setup (for Python-only issues)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> You can run and test individual service functions without Docker for issues like entity extraction and ingestion parsing.

### 6. Frontend-only setup

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
SignalGraph-AI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings (env vars)
│   │   ├── database.py          # DB connection & session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic (ingestion, retrieval, etc.)
│   │   ├── routers/             # FastAPI route handlers
│   │   └── utils/               # Helpers (text chunking, etc.)
│   └── tests/                   # pytest tests
├── frontend/
│   └── src/
│       ├── pages/               # One file per page
│       ├── components/          # Shared UI components
│       ├── api/                 # API client
│       └── types/               # TypeScript types
├── sample-data/                 # Sample incident/runbook files
└── docker-compose.yml
```

---

## Finding an Issue to Work On

### 🟢 New to the project? Start here:

Look for issues labelled **`good first issue`**:
👉 [View good first issues](https://github.com/AbaSheger/SignalGraph-AI/issues?q=is%3Aopen+label%3A%22good+first+issue%22)

**Recommended starting points:**

| Issue | Why it's great for beginners |
|---|---|
| 🧠 Entity extraction (#4) | Pure Python + regex, no Docker needed |
| 📥 Ingestion pipeline (#3) | Well-scoped, Python only, clear file targets |
| 📊 Pattern detection (#8) | SQL GROUP BY queries in Python, very concrete |

### Claiming an issue

1. Comment on the issue: _"I'd like to work on this!"_
2. Wait for a maintainer to assign it to you (or self-assign if you have permissions)
3. Create a branch and start working

---

## Making a Contribution

### Branch naming

Use this format:

```
feat/<issue-number>-short-description
fix/<issue-number>-short-description
docs/<short-description>
```

Examples:
```
feat/4-entity-extraction
fix/3-markdown-parsing
docs/contributing-guide
```

### Workflow

```bash
# 1. Create a branch from main
git checkout -b feat/4-entity-extraction

# 2. Make your changes
# 3. Run tests (see below)
# 4. Commit with a clear message
git commit -m "feat: add entity extraction for service_name and error_type"

# 5. Push and open a PR
git push origin feat/4-entity-extraction
```

---

## Coding Guidelines

### Python (backend)

- **Python 3.11+**, type hints on all functions
- **One function = one responsibility** — keep functions small and named clearly
- **No business logic in routers** — routers call service functions only
- **Pydantic schemas** for all request/response shapes
- **Comments** only where logic is non-obvious
- Format with `black` and lint with `ruff`:

```bash
pip install black ruff
black backend/
ruff check backend/
```

### TypeScript (frontend)

- **Strict mode** TypeScript — no `any`
- All API calls go through `src/api/client.ts`
- Shared types in `src/types/index.ts`
- Format with Prettier:

```bash
cd frontend
npm run format
npm run lint
```

---

## Running Tests

### Backend (pytest)

```bash
cd backend
pytest                          # run all tests
pytest tests/test_ingestion.py  # run a specific test file
pytest -v                       # verbose output
pytest -k "test_chunking"       # run tests matching a name
```

### Frontend (Vitest)

```bash
cd frontend
npm run test
npm run test -- --watch         # watch mode
```

> ✅ All tests must pass before opening a PR. If you're adding a new feature, add tests for it.

---

## Submitting a Pull Request

1. **Make sure all tests pass** locally
2. **Keep PRs focused** — one issue per PR
3. **Fill in the PR template** — describe what you changed and why
4. **Link the issue** in your PR description: `Closes #4`
5. **Request a review** from a maintainer

### PR checklist

- [ ] Tests pass locally (`pytest` / `npm run test`)
- [ ] New functionality has tests
- [ ] Code follows the style guidelines
- [ ] PR description explains what was changed and why
- [ ] Issue is linked with `Closes #<number>`

---

## Getting Help

Stuck? Don't worry — ask for help!

- 💬 **Comment on the issue** you're working on — maintainers check regularly
- 📖 **Check the README** for architecture overview and quick start
- 🔍 **Browse existing code** — the patterns repeat, so reading one service helps you understand others

We want you to succeed. No question is too basic. 🙌

---

## Thank You

Every contribution makes SignalGraph AI better. Whether it's fixing a typo, writing a test, or implementing a full feature — we appreciate your time and effort. 💙
