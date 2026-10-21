# JobAstra AI — AI-Powered Career Agent

JobAstra AI is the Python AI service for the broader [JobAstra platform](https://github.com/ankitsharma34/JobAstra). It turns resumes and job postings into validated data, builds a user-scoped career knowledge base, retrieves evidence with semantic search, evaluates job fit, drafts grounded application answers, and exposes the same capabilities as LangChain tools to a local single agent.

The repository is an active development MVP. Authentication, production observability, comprehensive tests, and failure-safe indexing remain incomplete.

## Implemented features

- PDF resume text extraction and structured career-profile extraction
- Structured job-description extraction with required/preferred qualification separation
- Local embedding models and PostgreSQL/pgvector storage
- Stable career documents, metadata-preserving chunking, and profile replacement
- User-filtered semantic retrieval and grounded career Q&A with source attribution
- LLM-based heuristic job matching with evidence references
- Evidence-grounded application-answer drafts with sensitive-question safeguards
- Four user-bound LangChain tools and a local single-agent runner
- Multiple configurable chat providers behind one `LLMService`

## Architecture

```mermaid
flowchart LR
    Client[API client or local CLI] --> API[FastAPI routes]
    Client --> Agent[JobAstra agent]
    API --> Services[Domain services]
    Agent --> Tools[LangChain tools]
    Tools --> Services
    Services --> LLM[LLMService]
    LLM --> Provider[Configured chat provider]
    Services --> Retriever[CareerRetriever]
    Retriever --> PG[(PostgreSQL + pgvector)]
    Ingest[CareerKnowledgeService] --> Docs[Documents + chunks]
    Docs --> Embed[Local embedding model]
    Embed --> PG
```

## Technology stack

| Area | Technology |
|---|---|
| API and validation | Python 3.12+, FastAPI, Pydantic v2, pydantic-settings |
| LLM orchestration | LangChain and configurable chat providers |
| Retrieval | Local embedding models and PGVector |
| Documents | pypdf, RecursiveCharacterTextSplitter |
| Storage | PostgreSQL 17 with pgvector, psycopg 3 |
| Tooling | uv, Ruff, pytest, Docker Compose |

## Quick start

Prerequisites: Python 3.12+, [uv](https://docs.astral.sh/uv/), Docker, and an API key for a supported chat provider.

```bash
uv sync
copy .env.example .env
docker compose up -d
uv run uvicorn jobastra_ai.main:app --app-dir src --reload
```

Use `cp` instead of `copy` on macOS/Linux. Configure `.env` first:

```ini
LLM_PROVIDER=your-provider-name
LLM_MODEL=your-chat-model-name
LLM_API_KEY=your-provider-api-key
LLM_TEMPERATURE=0
LLM_TIMEOUT=30
LLM_MAX_RETRIES=3
EMBEDDING_MODEL=your-embedding-model-name
EMBEDDING_DEVICE=cpu
VECTOR_DATABASE_URL=postgresql+psycopg://jobastra:jobastra@localhost:5432/jobastra
VECTOR_COLLECTION_NAME=career_knowledge
```

OpenAPI is at `http://127.0.0.1:8000/docs`. Useful commands:

```bash
uv run pytest
uv run ruff check .
uv run python scripts/check_llm.py
uv run python scripts/run_agent.py --user-id user-123 --profile career-profile.json
```

Create private `career-profile.json` from `career-profile.example.json`; it is ignored by Git.

## Project structure

```text
src/jobastra_ai/
├── api/             # routes, dependencies, errors
├── llm/             # provider-neutral model boundary
├── career/          # profile schemas and extraction
├── jobs/            # job schemas and extraction
├── embeddings/      # local embedding model
├── knowledge/       # documents, chunking, PGVector, ingestion
├── rag/             # retrieval and grounded Q&A
├── matching/        # evidence-grounded fit assessment
├── applications/    # grounded application drafts
├── tools/           # LangChain tools and registry
└── agent/           # single-agent runtime
```

## API overview

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness response |
| POST | `/api/career/profile/extract` | Extract a profile from a PDF |
| POST | `/api/jobs/extract` | Extract a job description |
| POST | `/api/career/knowledge/index` | Manually index a profile |
| POST | `/api/career/rag/answer` | Answer from career evidence |
| POST | `/api/jobs/match` | Evaluate profile/job fit |
| POST | `/api/applications/answer` | Draft an application answer |

See the [API reference](docs/06-api-reference.md), including authentication limitations.

## Documentation

Start at the [documentation index](docs/README.md). Key guides cover [architecture](docs/02-system-architecture.md), [setup](docs/05-setup-and-configuration.md), [RAG](docs/12-career-rag.md), [the agent](docs/16-single-agent.md), and [security](docs/19-security-and-reliability.md).

To change chat models or integrate another LLM provider, follow [Adding models and providers](docs/22-adding-models-and-providers.md).

To replace the local embedding model safely, follow [Changing the embedding model](docs/23-changing-embedding-model.md).

## Roadmap

Planned work includes complete authentication, transactional profile replacement, retrieval evaluation, score calibration, production telemetry, broader tests, conversation persistence, OCR, and deployment hardening. See the [roadmap](docs/21-future-roadmap.md).
