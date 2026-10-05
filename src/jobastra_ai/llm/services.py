from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from jobastra_ai.llm.config import LLMSettings, get_llm_settings
from jobastra_ai.llm.models import create_chat_model, get_chat_model
from jobastra_ai.llm.schemas import LLMMessage, LLMRequest, LLMResponse


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

        result = self._model.invoke(self._to_langchain_messages(request.messages))
        return self._to_response(result)

    async def ainvoke(self, request: LLMRequest) -> LLMResponse:
        """Asynchronously invoke the configured model."""

        result = await self._model.ainvoke(self._to_langchain_messages(request.messages))
        return self._to_response(result)

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
