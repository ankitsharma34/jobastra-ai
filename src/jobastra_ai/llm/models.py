from functools import lru_cache

from langchain_core.language_models import BaseChatModel
from langchain_mistralai import ChatMistralAI

from jobastra_ai.llm.config import LLMSettings, get_llm_settings


def create_chat_model(settings: LLMSettings) -> BaseChatModel:
    """Create the chat model configured for the application."""

    provider = settings.provider.strip().lower()

    if provider in {"mistral", "mistralai"}:
        return ChatMistralAI(
            model=settings.model,
            api_key=settings.api_key,
            temperature=settings.temperature,
            timeout=settings.timeout,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.provider!r}")


@lru_cache
def get_chat_model() -> BaseChatModel:
    """Return the shared chat model instance."""

    return create_chat_model(get_llm_settings())