from typing import TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError

from jobastra_ai.llm.config import LLMSettings, get_llm_settings
from jobastra_ai.llm.errors import LLMInvocationError, LLMOutputValidationError
from jobastra_ai.llm.models import create_chat_model, get_chat_model
from jobastra_ai.llm.schemas import LLMMessage, LLMRequest, LLMResponse

StructuredOutputT = TypeVar("StructuredOutputT", bound=BaseModel)


class LLMService:
    """Provider-neutral boundary around LangChain chat models."""

    def __init__(
        self,
        model: BaseChatModel | None = None,
        settings: LLMSettings | None = None,
    ) -> None:
        self._settings = settings or get_llm_settings()
        self._model = model or (
            create_chat_model(settings) if settings is not None else get_chat_model()
        )

    def invoke(self, request: LLMRequest) -> LLMResponse:
        """Invoke the configured model and return a JobAstra response."""

        try:
            result = self._model.invoke(self._to_langchain_messages(request.messages))
            return self._to_response(result)
        except LLMInvocationError:
            raise
        except Exception as exc:
            raise self._invocation_error() from exc

    async def ainvoke(self, request: LLMRequest) -> LLMResponse:
        """Asynchronously invoke the configured model."""

        try:
            result = await self._model.ainvoke(self._to_langchain_messages(request.messages))
            return self._to_response(result)
        except LLMInvocationError:
            raise
        except Exception as exc:
            raise self._invocation_error() from exc

    def invoke_structured(
        self,
        request: LLMRequest,
        output_schema: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Invoke the model and validate its output against a Pydantic schema."""

        try:
            structured_model = self._model.with_structured_output(output_schema)
            result = structured_model.invoke(self._to_langchain_messages(request.messages))
        except ValidationError as exc:
            raise self._output_validation_error() from exc
        except Exception as exc:
            raise self._invocation_error() from exc
        return self._validate_structured_output(result, output_schema)

    async def ainvoke_structured(
        self,
        request: LLMRequest,
        output_schema: type[StructuredOutputT],
    ) -> StructuredOutputT:
        """Asynchronously invoke the model and return validated structured output."""

        try:
            structured_model = self._model.with_structured_output(output_schema)
            result = await structured_model.ainvoke(self._to_langchain_messages(request.messages))
        except ValidationError as exc:
            raise self._output_validation_error() from exc
        except Exception as exc:
            raise self._invocation_error() from exc
        return self._validate_structured_output(result, output_schema)

    @staticmethod
    def _to_langchain_messages(messages: list[LLMMessage]) -> list[BaseMessage]:
        message_types = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage,
        }
        return [message_types[message.role](content=message.content) for message in messages]

    def _to_response(self, message: BaseMessage) -> LLMResponse:
        return LLMResponse(
            content=message.text,
            model=self._settings.model,
            provider=self._settings.provider,
        )

    @staticmethod
    def _validate_structured_output(
        result: object,
        output_schema: type[StructuredOutputT],
    ) -> StructuredOutputT:
        if isinstance(result, output_schema):
            return result
        try:
            return output_schema.model_validate(result)
        except ValidationError as exc:
            raise LLMService._output_validation_error() from exc

    def _invocation_error(self) -> LLMInvocationError:
        return LLMInvocationError(f"The {self._settings.provider} model invocation failed")

    @staticmethod
    def _output_validation_error() -> LLMOutputValidationError:
        return LLMOutputValidationError(
            "The model returned output that does not match the requested schema"
        )
