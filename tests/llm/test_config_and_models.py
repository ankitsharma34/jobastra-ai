import pytest
from pydantic import ValidationError

from jobastra_ai.llm.schemas import LLMMessage, LLMRequest, LLMResponse


@pytest.mark.parametrize("role", ["system", "user", "assistant"])
def test_llm_message_accepts_supported_roles(role: str) -> None:
    message = LLMMessage(role=role, content="Hello")  # type: ignore[arg-type]

    assert message.role == role


def test_llm_message_rejects_unknown_role() -> None:
    with pytest.raises(ValidationError):
        LLMMessage(role="tool", content="Hello")  # type: ignore[arg-type]


def test_llm_request_requires_at_least_one_message() -> None:
    with pytest.raises(ValidationError):
        LLMRequest(messages=[])


def test_llm_schemas_reject_unexpected_fields() -> None:
    with pytest.raises(ValidationError):
        LLMResponse(
            content="Hello",
            model="test-model",
            provider="test-provider",
            unexpected=True,  # type: ignore[call-arg]
        )


def test_llm_response_preserves_provider_metadata() -> None:
    response = LLMResponse(
        content="Hello",
        model="test-model",
        provider="test-provider",
    )

    assert response.model_dump() == {
        "content": "Hello",
        "model": "test-model",
        "provider": "test-provider",
    }
