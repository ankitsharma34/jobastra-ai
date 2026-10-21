# System architecture

```mermaid
flowchart TD
    Routes[FastAPI routes] --> DI[Dependency factories]
    DI --> Domain[Domain services]
    CLI[Local runner] --> Registry[Tool registry]
    Registry --> Tools[Structured tools]
    Tools --> Domain
    Domain --> LLM[LLMService]
    LLM --> Model[BaseChatModel]
    Model --> Remote[Configured chat provider]
    Domain --> Retriever[CareerRetriever]
    Retriever --> Store[CareerPGVector]
    Ingest[CareerKnowledgeService] --> Builder[Document builder]
    Builder --> Chunker[Chunker]
    Chunker --> Store
    Store --> Embed[Cached embeddings]
    Store --> DB[(PostgreSQL + pgvector)]
```

Routes and tools are delivery adapters around the same services. `LLMService` isolates providers; `CareerRetriever` isolates search; `knowledge/store.py` isolates PostgreSQL. `get_chat_model`, `get_embedding_model`, and `get_vector_store` use `lru_cache`, while lightweight service wrappers are created by FastAPI dependencies.

Remote inference dominates generation latency. PDF parsing runs in a thread pool; model and vector operations use async APIs. The repository has no queue, circuit breaker, or explicit backpressure.
