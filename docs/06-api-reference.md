# API reference

All routes use `/api`; interactive OpenAPI is at `/docs`.

| Route | Contract | Notes |
|---|---|---|
| `GET /api/health` | status object | Liveness only |
| `POST /api/career/profile/extract` | multipart PDF → `CareerProfile` | PDF only, 10 MB |
| `POST /api/jobs/extract` | extraction request → `JobDescription` | raw job text |
| `POST /api/career/knowledge/index` | IDs/profile → 204 | development identity |
| `POST /api/career/rag/answer` | `CareerRAGRequest/Response` | top-k 1–10 |
| `POST /api/jobs/match` | `JobMatchRequest/Result` | LLM heuristic |
| `POST /api/applications/answer` | payload → response | request-state identity |

```json
{"job_text":"Backend Engineer. Required: Python. Docker preferred.","additional_context":null}
```

The application route reads `request.state.user_id`; no middleware here sets it, so standalone requests return 401 unless integration code supplies it. Knowledge, RAG, and matching accept `user_id` in request bodies.

Validation returns 422. PDF failures use 422, unsupported media 415, and oversized files 413. LLM timeouts use 504; invocation/structured-output failures 502; configuration errors a sanitized 500. Database failures currently fall through to generic 500.
