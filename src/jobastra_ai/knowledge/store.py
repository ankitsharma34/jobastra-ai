from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector

from jobastra_ai.embeddings.models import get_embedding_model
from jobastra_ai.knowledge.config import (
    VectorStoreSettings,
    get_vector_store_settings,
)


def create_vector_store(
    settings: VectorStoreSettings,
    embedding_model: Embeddings,
) -> PGVector:
    """Create the PostgreSQL-backed career knowledge vector store."""

    return PGVector(
        embeddings=embedding_model,
        connection=settings.database_url.get_secret_value(),
        collection_name=settings.collection_name,
        use_jsonb=True,
        async_mode=True,
    )


@lru_cache(maxsize=1)
def get_vector_store() -> PGVector:
    """Return the shared vector store and its reusable database connection pool."""

    return create_vector_store(
        get_vector_store_settings(),
        get_embedding_model(),
    )
