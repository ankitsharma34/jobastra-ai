from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector

from jobastra_ai.embeddings.models import get_embedding_model
from jobastra_ai.knowledge.config import (
    VectorStoreSettings,
    get_vector_store_settings,
)


class CareerPGVector(PGVector):
    """PGVector store with user-scoped profile replacement support."""

    async def adelete_by_metadata(self, metadata_filter: dict[str, str]) -> None:
        if not metadata_filter:
            raise ValueError("metadata_filter must not be empty")

        await self.__apost_init__()
        async with self._make_async_session() as session:
            collection = await self.aget_collection(session)
            if collection is None:
                return

            statement = self.EmbeddingStore.__table__.delete().where(
                self.EmbeddingStore.collection_id == collection.uuid,
                self._create_filter_clause(metadata_filter),
            )
            await session.execute(statement)
            await session.commit()


def create_vector_store(
    settings: VectorStoreSettings,
    embedding_model: Embeddings,
) -> CareerPGVector:
    """Create the PostgreSQL-backed career knowledge vector store."""

    return CareerPGVector(
        embeddings=embedding_model,
        connection=settings.database_url.get_secret_value(),
        collection_name=settings.collection_name,
        use_jsonb=True,
        async_mode=True,
    )


@lru_cache(maxsize=1)
def get_vector_store() -> CareerPGVector:
    """Return the shared vector store and its reusable database connection pool."""

    return create_vector_store(
        get_vector_store_settings(),
        get_embedding_model(),
    )
