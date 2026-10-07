from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel

from jobastra_ai.llm.config import LLMSettings
from jobastra_ai.llm.errors import (
    LLMInvocationError,
    LLMOutputValidationError,
    LLMTimeoutError,
)
from jobastra_ai.llm.schemas import LLMMessage, LLMRequest
from jobastra_ai.llm.services import LLMService


class ScoreOutput(BaseModel):
    score: int
    reason: str


@pytest.fixture
def settings() -> LLMSettings:
    return LLMSettings(
        _env_file=None,
        provider="test-provider",
        model="test-model",
        api_key="test-key",
        timeout=5,
    )


@pytest.fixture
def llm_request() -> LLMRequest:
    return LLMRequest(
        messages=[
            LLMMessage(role="system", content="Follow instructions."),
            LLMMessage(role="user", content="Score this job."),
            LLMMessage(role="assistant", content="Understood."),
        ]
    )


def test_invoke_translates_messages_and_response(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.invoke.return_value = AIMessage(content="A strong match")
    service = LLMService(model=model, settings=settings)

    response = service.invoke(llm_request)

    messages = model.invoke.call_args.args[0]
    assert [type(message) for message in messages] == [
        SystemMessage,
        HumanMessage,
        AIMessage,
    ]
    assert [message.text for message in messages] == [
        "Follow instructions.",
        "Score this job.",
        "Understood.",
    ]
    assert response.model_dump() == {
        "content": "A strong match",
        "model": "test-model",
        "provider": "test-provider",
    }


async def test_ainvoke_returns_normalized_response(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.ainvoke = AsyncMock(return_value=AIMessage(content="Async result"))
    service = LLMService(model=model, settings=settings)

    response = await service.ainvoke(llm_request)

    assert response.content == "Async result"
    model.ainvoke.assert_awaited_once()


def test_invoke_structured_returns_validated_model(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.with_structured_output.return_value = RunnableLambda(
        lambda _: {"score": 91, "reason": "Relevant experience"}
    )
    service = LLMService(model=model, settings=settings)

    result = service.invoke_structured(llm_request, ScoreOutput)

    assert result == ScoreOutput(score=91, reason="Relevant experience")
    model.with_structured_output.assert_called_once_with(ScoreOutput)


async def test_ainvoke_structured_returns_validated_model(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.with_structured_output.return_value = RunnableLambda(
        lambda _: ScoreOutput(score=88, reason="Good skills overlap")
    )
    service = LLMService(model=model, settings=settings)

    result = await service.ainvoke_structured(llm_request, ScoreOutput)

    assert result.score == 88


def test_structured_output_validation_error_is_translated(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.with_structured_output.return_value = RunnableLambda(lambda _: {"score": "not-a-number"})
    service = LLMService(model=model, settings=settings)

    with pytest.raises(LLMOutputValidationError) as error:
        service.invoke_structured(llm_request, ScoreOutput)

    assert "requested schema" in str(error.value)
    assert error.value.__cause__ is not None


def test_provider_error_is_translated_without_leaking_details(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.invoke.side_effect = RuntimeError("sensitive provider response")
    service = LLMService(model=model, settings=settings)

    with pytest.raises(LLMInvocationError) as error:
        service.invoke(llm_request)

    assert "test-provider" in str(error.value)
    assert "sensitive provider response" not in str(error.value)
    assert isinstance(error.value.__cause__, RuntimeError)


@pytest.mark.parametrize(
    "timeout_error",
    [TimeoutError("slow"), httpx.ReadTimeout("slow")],
)
def test_timeout_error_is_classified(
    settings: LLMSettings,
    llm_request: LLMRequest,
    timeout_error: Exception,
) -> None:
    model = Mock(spec=BaseChatModel)
    model.invoke.side_effect = timeout_error
    service = LLMService(model=model, settings=settings)

    with pytest.raises(LLMTimeoutError, match="timed out after 5 seconds"):
        service.invoke(llm_request)


def test_nested_timeout_error_is_classified(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    timeout = TimeoutError("slow")
    wrapped = RuntimeError("provider wrapper")
    wrapped.__cause__ = timeout
    model = Mock(spec=BaseChatModel)
    model.invoke.side_effect = wrapped
    service = LLMService(model=model, settings=settings)

    with pytest.raises(LLMTimeoutError):
        service.invoke(llm_request)


def test_existing_llm_invocation_error_is_not_wrapped(
    settings: LLMSettings,
    llm_request: LLMRequest,
) -> None:
    original = LLMInvocationError("already translated")
    model = Mock(spec=BaseChatModel)
    model.invoke.side_effect = original
    service = LLMService(model=model, settings=settings)

    with pytest.raises(LLMInvocationError) as error:
        service.invoke(llm_request)

    assert error.value is original
