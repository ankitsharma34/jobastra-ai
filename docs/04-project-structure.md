# Project structure

```text
scripts/                  # LLM check and local agent
tests/                    # health and LLM tests
src/jobastra_ai/
├── main.py, core/, api/  # app, settings, routes, DI, HTTP errors
├── llm/, prompts/        # model boundary and prompt primitives
├── documents/, career/   # PDF/profile extraction
├── jobs/                 # job extraction
├── embeddings/, knowledge/ # vectors, documents, store, ingestion
├── rag/, matching/       # retrieval, Q&A, fit assessment
├── applications/         # grounded drafts
├── tools/                # tool factories and registry
└── agent/                # prompt, factory, runtime
```

Most domains follow `schemas.py → prompts.py → service.py`. HTTP and tool layers delegate to services. Provider-specific code stays under `llm/`; PGVector-specific code stays under `knowledge/`.
