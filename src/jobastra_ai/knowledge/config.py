from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class VectorStoreSettings(BaseSettings):
    """Configuration for career knowledge vector storage."""

    database_url: SecretStr
    collection_name: str = Field(min_length=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VECTOR_",
        extra="ignore",
    )


@lru_cache
def get_vector_store_settings() -> VectorStoreSettings:
    """Return cached vector store settings loaded from the environment."""

    return VectorStoreSettings()
