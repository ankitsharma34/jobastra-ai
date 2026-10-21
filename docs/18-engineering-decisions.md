# Engineering decisions and trade-offs

These rationales are architectural interpretations of the code, not claims about undocumented historical decisions.

| Decision | Repository choice | Benefits | Costs / choose an alternative when |
|---|---|---|---|
| Python vs TypeScript | Python 3.12 | Mature ML/embedding ecosystem, concise async services | TypeScript may fit a Node-only team or shared full-stack types |
| FastAPI vs Flask/Django | FastAPI | Pydantic/OpenAPI/async/DI | Django fits a full ORM/admin product; Flask fits a tiny API |
| LangChain vs SDKs | LangChain abstractions | Provider-neutral models, tools, documents, agent | Direct SDK gives tighter provider control and fewer layers |
| Structured output vs parsing JSON text | Provider structured output + Pydantic | Typed contracts and explicit failures | Free text is suitable when no machine contract is required |
| Local vs hosted embeddings | Local embedding model | Privacy, predictable marginal cost, offline inference after download | Hosted models can offer quality/operations at usage cost |
| PostgreSQL/pgvector vs FAISS/dedicated DB | PGVector | Persistence, metadata filters, one operational store | FAISS fits local experiments; managed vector DB fits very large/distributed workloads |
| RAG vs full profile in every prompt | Source documents + top-k | Smaller relevant context and attribution | Full profile may be simpler for small, always-required profiles |
| LLM matching vs deterministic rubric | LLM heuristic | Nuance and project relevance | Deterministic/hybrid scoring is better for consistency/auditability |
| Agent vs fixed workflow | Agent only in local runner | Flexible tool selection for open-ended requests | API services use deterministic flows where steps are known |
| Single vs multiple agents | One agent | Simpler execution and fewer coordination failures | Specialization may help only after complexity/evaluation justifies it |
| Async vs sync | Async network/vector services; thread-pooled PDF | Better I/O concurrency | CPU-heavy embedding still needs capacity planning/workers |
| Separate AI service vs monolith | Standalone repository/service | Independent Python dependencies and AI evolution | A monolith can simplify early deployment and transactions |

Stable domain services behind adapters are the key maintainability choice. The notable coupling is `CareerPGVector` reaching into protected PGVector internals for metadata deletion; library upgrades require care.
