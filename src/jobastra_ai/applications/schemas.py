from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.jobs.schemas import JobDescription
from jobastra_ai.rag.schemas import CareerEvidence


class ApplicationSchema(BaseModel):
    """Base configuration shared by application answer schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ApplicationAnswerRequest(ApplicationSchema):
    """Request for a career-grounded application answer.

    The user ID is accepted for the development API only. Production callers
    should receive it from trusted authentication context.
    """

    user_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    job: JobDescription
    max_words: int | None = Field(default=None, ge=10, le=1000)
    additional_instructions: str | None = Field(default=None, min_length=1)


class ApplicationAnswerResponse(ApplicationSchema):
    answer: str | None = Field(min_length=1)
    sources: list[CareerEvidence]
    needs_user_input: bool
    missing_information: list[str]
