from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """Configuration for the language model."""

    provider: str
    model: str
    api_key: SecretStr
    temperature: float = 0.0
    timeout: float = Field(default=30.0, gt=0)
    max_retries: int = Field(default=3, ge=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LLM_",
        extra="ignore",
    )


@lru_cache
def get_llm_settings() -> LLMSettings:
    """Return the cached LLM settings loaded from the environment."""
    return LLMSettings()
