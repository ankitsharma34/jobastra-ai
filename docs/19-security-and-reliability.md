# Security and reliability

## Currently implemented

- Secrets load from `.env`; API keys/database URLs use `SecretStr` in settings.
- Most domain schemas forbid extra fields, strip whitespace, constrain bounds/enums, and validate dates.
- PDF routes enforce MIME allow-list, nonempty content, and a 10 MB limit; encrypted/scanned-only PDFs fail safely.
- Retrieval always applies a `user_id` metadata filter; tools bind user identity outside model-generated arguments.
- RAG/job/application prompts label external text as untrusted data and prohibit following embedded instructions.
- RAG removes unknown source references; matching and application services filter returned references against retrieved evidence.
- Sensitive application declarations are blocked when matching evidence is missing.
- Agent execution has recursion limit 20 and exposes a sanitized failure.
- LLM provider details are wrapped; API exception handlers avoid raw upstream messages.

## Known limitations

- No authentication middleware is implemented. Application answers are unusable standalone without injected request state; RAG, matching, and indexing trust body `user_id`.
- Metadata filtering is an application condition, not database row-level security. A regression could leak career data.
- Career content is sensitive and stored in PostgreSQL; encryption, retention, deletion APIs, backups, and audit policy are unspecified.
- Prompt rules reduce injection risk but cannot guarantee instruction isolation.
- Profile replacement deletes before insert and is not transactional.
- No request rate limiting, quotas, circuit breaker, health dependency checks, telemetry, or database error translation.
- Tool traces and agent decisions are not audited; tool failures end the request.
- Provider retries can amplify latency/cost; one provider adapter currently has mismatched timeout units.
- No malware scanning, OCR safety pipeline, or PDF processing sandbox is present.

## Recommended improvements

Add verified auth middleware and derive identity for every endpoint; enforce PostgreSQL row-level security or equivalent tenant boundaries; make replacement transactional/staged; add secret management, encryption/retention/deletion controls, rate limits, structured logs/traces, dependency readiness checks, provider fallback/circuit breaking, prompt-injection tests, and human approval for consequential actions. Keep application submission outside agent authority unless an explicit reviewed approval workflow is built.

If another user's result appears, fail closed, disable the affected path, inspect logs, fix authorization and database policy, notify according to incident policy, and add regression tests. Semantic filters alone are not authorization.
