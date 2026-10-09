from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbeddingSettings(BaseSettings):
    """Configuration for the embedding model."""

    model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        min_length=1,
    )
    device: str = Field(default="cpu", min_length=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EMBEDDING_",
        extra="ignore",
    )


@lru_cache
def get_embedding_settings() -> EmbeddingSettings:
    """Return cached embedding settings loaded from the environment."""

    return EmbeddingSettings()
