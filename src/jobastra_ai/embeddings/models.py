from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from jobastra_ai.embeddings.config import EmbeddingSettings, get_embedding_settings


def create_embedding_model(settings: EmbeddingSettings) -> Embeddings:
    """Create the embedding model configured for the application."""

    return HuggingFaceEmbeddings(
        model=settings.model,
        model_kwargs={"device": settings.device},
    )


@lru_cache(maxsize=1)
def get_embedding_model() -> Embeddings:
    """Return the shared embedding model instance."""

    return create_embedding_model(get_embedding_settings())
