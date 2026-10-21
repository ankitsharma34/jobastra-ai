# Testing and debugging

## Existing coverage

`tests/test_health.py` verifies `/api/health`. `tests/llm/test_schemas.py` checks roles, nonempty requests, forbidden fields, and metadata. `tests/llm/test_services.py` covers message translation, sync/async invocation, structured validation, provider-error sanitization, and direct/nested timeout classification.

`tests/llm/test_config_and_models.py` currently duplicates schema tests despite its filename; it does not test settings or provider factories. There are no automated tests for PDF parsing, career/job services, documents/chunking, PGVector ingestion, retrieval filters, RAG attribution, matching, application safeguards, tools, agent loops, or most routes. No coverage metric or AI evaluation dataset is configured.

```bash
uv run pytest
uv run ruff check .
uv run python scripts/check_llm.py
docker compose ps
docker compose logs postgres
```

`check_llm.py` directly invokes the configured provider and prints no progress before completion. A 401 means invalid provider credentials; 429 means a provider limit; network/timeout behavior depends on provider retry settings. `run_agent.py` wraps agent failures, so use `check_llm.py` to isolate chat connectivity first.

## Recommended test strategy

1. Unit-test schema validators, prompt rendering, document identity, chunk metadata, source filtering, and sensitive-question classification with fakes.
2. Contract-test each provider's structured output and tool calling behind an opt-in marker.
3. Integration-test PostgreSQL replacement and tenant filters in disposable Docker infrastructure.
4. API-test all status codes and dependency overrides, especially identity.
5. Build golden datasets for extraction, retrieval recall@k, citation precision, matching stability, hallucination rate, and answer faithfulness.
6. Agent-test expected tool sequences, repeated calls, malformed tool results, recursion exhaustion, and provider failure.

AI evaluations should compare outputs semantically and by schema/evidence support rather than exact wording.
