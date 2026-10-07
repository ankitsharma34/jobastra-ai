from collections.abc import Mapping
from string import Formatter
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from jobastra_ai.llm.schemas import LLMMessage, LLMRequest
from jobastra_ai.prompts.errors import PromptRenderError


class PromptMessageTemplate(BaseModel):
    """Template for one message in a provider-neutral chat prompt."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    role: Literal["system", "user", "assistant"]
    template: str = Field(min_length=1)


class PromptTemplate(BaseModel):
    """A named, versioned chat prompt that renders to an LLM request."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    version: str = Field(default="1", min_length=1)
    messages: tuple[PromptMessageTemplate, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_templates(self) -> Self:
        for message in self.messages:
            try:
                parsed_fields = tuple(Formatter().parse(message.template))
            except ValueError as exc:
                raise ValueError(f"Invalid template for {message.role} message") from exc
            if any(
                field_name is not None and (not field_name or field_name.isdecimal())
                for _, field_name, _, _ in parsed_fields
            ):
                raise ValueError("Prompt templates require named placeholders")
        return self

    @property
    def variables(self) -> frozenset[str]:
        """Return the top-level variable names required by this prompt."""

        variables: set[str] = set()
        for message in self.messages:
            for _, field_name, _, _ in Formatter().parse(message.template):
                if field_name:
                    root_name = field_name.split(".", 1)[0].split("[", 1)[0]
                    variables.add(root_name)
        return frozenset(variables)

    def render(self, variables: Mapping[str, Any] | None = None, /, **kwargs: Any) -> LLMRequest:
        """Render the prompt as an LLM request using the supplied variables."""

        context = dict(variables or {})
        context.update(kwargs)
        missing = self.variables.difference(context)
        if missing:
            names = ", ".join(sorted(missing))
            raise PromptRenderError(f"Missing prompt variables: {names}")

        try:
            messages = [
                LLMMessage(
                    role=message.role,
                    content=message.template.format_map(context),
                )
                for message in self.messages
            ]
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            raise PromptRenderError(f"Failed to render prompt {self.name!r}") from exc

        return LLMRequest(messages=messages)
