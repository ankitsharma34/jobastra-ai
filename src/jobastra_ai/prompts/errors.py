class PromptError(ValueError):
    """Base exception for prompt infrastructure errors."""


class PromptNotFoundError(PromptError):
    """Raised when a named prompt is not registered."""


class PromptAlreadyRegisteredError(PromptError):
    """Raised when a prompt name is registered more than once."""


class PromptRenderError(PromptError):
    """Raised when a prompt cannot be rendered with the supplied variables."""
