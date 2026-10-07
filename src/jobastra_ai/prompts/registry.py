from collections.abc import Iterator

from jobastra_ai.llm.schemas import LLMRequest
from jobastra_ai.prompts.errors import PromptAlreadyRegisteredError, PromptNotFoundError
from jobastra_ai.prompts.templates import PromptTemplate


class PromptRegistry:
    """In-memory registry for application prompt templates."""

    def __init__(self) -> None:
        self._prompts: dict[str, PromptTemplate] = {}

    def register(self, prompt: PromptTemplate, *, replace: bool = False) -> None:
        if prompt.name in self._prompts and not replace:
            raise PromptAlreadyRegisteredError(f"Prompt {prompt.name!r} is already registered")
        self._prompts[prompt.name] = prompt

    def get(self, name: str) -> PromptTemplate:
        try:
            return self._prompts[name]
        except KeyError as exc:
            raise PromptNotFoundError(f"Prompt {name!r} is not registered") from exc

    def render(self, name: str, **variables: object) -> LLMRequest:
        return self.get(name).render(variables)

    def __contains__(self, name: object) -> bool:
        return name in self._prompts

    def __iter__(self) -> Iterator[PromptTemplate]:
        return iter(self._prompts.values())

    def __len__(self) -> int:
        return len(self._prompts)


prompt_registry = PromptRegistry()
