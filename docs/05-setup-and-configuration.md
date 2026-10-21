# Setup and configuration

```bash
uv sync
copy .env.example .env
docker compose up -d
uv run uvicorn jobastra_ai.main:app --app-dir src --reload
```

Use `cp` on macOS/Linux. Compose starts pgvector PostgreSQL at port 5432 with development database/user/password `jobastra`.

| Variables | Meaning |
|---|---|
| `APP_NAME`, `APP_ENV`, `DEBUG` | application metadata/debug |
| `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY` | required chat configuration |
| `LLM_TEMPERATURE`, `LLM_TIMEOUT`, `LLM_MAX_RETRIES` | generation/runtime controls |
| `EMBEDDING_MODEL`, `EMBEDDING_DEVICE` | local embedding configuration |
| `VECTOR_DATABASE_URL`, `VECTOR_COLLECTION_NAME` | PGVector configuration |

Settings are cached; restart after `.env` changes. Never commit `.env` or `career-profile.json`.

Known issue: the generic timeout is described as seconds, but one supported provider adapter expects milliseconds; `models.py` currently forwards the rounded value. `LLM_TIMEOUT=30` therefore becomes roughly 30 ms for that adapter, while retries may extend the overall wait.

```bash
uv run python scripts/check_llm.py
uv run pytest
uv run ruff check .
docker compose logs postgres
```

The first embedding use may download weights. `HF_TOKEN` is optional.
