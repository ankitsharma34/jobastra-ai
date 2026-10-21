# Embeddings

Embeddings map text into dense numeric vectors. Texts with similar learned meaning tend to have nearby vectors, enabling semantic retrieval even when exact words differ. Cosine similarity compares vector direction; inner product and Euclidean distance are alternatives. The repository delegates the exact PGVector search operator/index behavior to `langchain-postgres` rather than implementing similarity math.

`EmbeddingSettings` independently loads `EMBEDDING_MODEL` and `EMBEDDING_DEVICE`. `create_embedding_model` returns the provider-neutral LangChain `Embeddings` interface backed by the configured local integration; `get_embedding_model` caches one instance. `EmbeddingService` validates strings and collections before async query/document embedding, although PGVector consumes the cached model directly.

```mermaid
flowchart LR
    Docs[Career chunks] --> DE[Document embeddings]
    Query[Question/job] --> QE[Query embedding]
    DE --> Store[(PGVector)]
    QE --> Search[Similarity search]
    Store --> Search
    Search --> TopK[Top-k documents]
```

The default approach uses a compact local model, reducing hosted API dependence and exposure. CPU inference is slower than GPU/hosted services. Semantic search can miss exact identifiers and can return plausible but irrelevant neighbors; hybrid lexical/vector search and reranking are future options. Model consistency is mandatory: re-index all rows after changing model or preprocessing.

Performance is roughly proportional to input count and model inference cost for embedding. Retrieval scalability depends on database indexing and corpus size; the application does not configure or tune ANN indexes itself.

For model-selection and re-indexing instructions, see [Changing the embedding model](23-changing-embedding-model.md).
