# Technology stack

| Layer | Choice | Role/trade-off |
|---|---|---|
| Runtime/API | Python 3.12, FastAPI, Uvicorn | Async API/OpenAPI; auth remains integration work |
| Contracts/settings | Pydantic v2, pydantic-settings | Strict validation and typed `.env` loading |
| AI orchestration | LangChain 1.4 | Shared models, tools, agents; framework coupling |
| Chat | Configurable remote providers | Provider selection behind `BaseChatModel` |
| Embeddings | Configurable local model | Local inference/data control; local compute cost |
| Retrieval | PostgreSQL 17, pgvector, langchain-postgres | SQL and vectors in one database |
| Documents | pypdf, text splitters | Embedded PDF text and recursive chunks |
| Engineering | uv, Ruff, pytest | Locking, linting, tests |

The configured embedding model determines vector dimensions; the code does not enforce a particular dimension. Changing the model requires re-indexing because queries and documents must use the same vector space.
