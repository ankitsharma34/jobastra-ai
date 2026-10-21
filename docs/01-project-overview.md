# Project overview

JobAstra AI is a standalone AI/backend service for career data. It extracts facts from resumes and job postings, converts career data into searchable evidence, and uses that evidence for Q&A, fit assessment, and application drafts. Separating it from the linked JobAstra application keeps model, retrieval, and agent dependencies in Python.

There are three entry styles: FastAPI routes, reusable domain services, and `scripts/run_agent.py`. The API does not expose the agent. The agent handles independent messages with no persistent history.

Evidence grounding is central: `CareerProfile` becomes user-tagged documents; semantic retrieval supplies context; prompts prohibit unsupported claims. Matching remains an LLM judgment, and its score is a heuristic rather than a hiring probability.

## Verified boundaries

- PDF parsing handles embedded text only; no OCR/DOCX.
- PGVector stores vectors; there are no domain ORM models.
- Application answers are drafts; submission is absent.
- No auth middleware is present. Application answers require externally populated request state; several development endpoints accept body `user_id`.
- No frontend, background queue, migrations, evaluation suite, deployment manifests, or conversation store exists.

JobAstra is an evidence-grounded career AI MVP with explicit provider, domain, retrieval, tool, and API boundaries. It is not a production hiring system.
