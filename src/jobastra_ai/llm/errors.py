class LLMError(RuntimeError):
    """Base exception for errors raised by the LLM layer."""


class LLMConfigurationError(LLMError):
    """Raised when the configured model cannot be created."""


class LLMInvocationError(LLMError):
    """Raised when a model invocation fails."""


class LLMOutputValidationError(LLMError):
    """Raised when model output does not match the requested schema."""
