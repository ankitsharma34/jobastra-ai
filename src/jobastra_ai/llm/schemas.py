from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LLMMessage(BaseModel):
    """A single provider-neutral chat message."""

    model_config = ConfigDict(extra="forbid")
    role: Literal["system", "user", "assistant"]
    content: str


class LLMRequest(BaseModel):
    """Input payload for a chat model invocation."""

    model_config = ConfigDict(extra="forbid")
    messages: list[LLMMessage] = Field(min_length=1)


class LLMResponse(BaseModel):
    """Provider-neutral response returned by a chat model."""

    model_config = ConfigDict(extra="forbid")
    content: str
    model: str
    provider: str
