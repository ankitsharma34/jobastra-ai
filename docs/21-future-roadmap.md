# Future roadmap

Everything below is planned/recommended rather than implemented.

## Highest priority

1. Add authentication middleware and derive identity for every user-scoped API/service; add DB-level tenant controls.
2. Correct provider-adapter timeout units and add bounded provider fallback/circuit breaking.
3. Make profile replacement failure-safe with transactions or versioned staging/swap.
4. Add tests for routes, domain services, tenant filtering, PGVector integration, tools, and agent behavior.
5. Build labeled extraction/retrieval/faithfulness/matching evaluation datasets.

## Product and AI quality

- Add similarity thresholds, hybrid retrieval, reranking, query rewriting, and evidence sufficiency.
- Replace or complement heuristic match scoring with transparent calibrated components and fairness review.
- Add claim-level answer verification, citation coverage, and word-count enforcement.
- Support human profile correction, source versioning, deletion/retention controls, and re-index status.
- Add OCR and possibly DOCX only after threat modeling and quality evaluation.

## Operations and agent evolution

- Queue/batch ingestion, separate CPU/GPU embedding workers, and tune vector indexes based on measurements.
- Add structured logs, traces, token/cost/latency metrics, readiness probes, rate limits, and audit events.
- Add conversation persistence only with privacy/retention controls.
- Add explicit approval nodes before any future external side effect. Application submission is not currently a capability.
- Consider explicit LangGraph workflows or multiple agents only when evaluation shows the single-agent design is insufficient.
