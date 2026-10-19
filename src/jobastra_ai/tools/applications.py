from typing import Any

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.applications.schemas import ApplicationAnswerRequest
from jobastra_ai.applications.service import ApplicationAnswerService
from jobastra_ai.jobs.schemas import JobDescription


class ApplicationAnswerGenerationInput(BaseModel):
    """Arguments available to the model when drafting an application answer."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    question: str = Field(min_length=1)
    job: JobDescription
    max_words: int | None = Field(default=None, ge=10, le=1000)


def create_application_answer_tool(
    service: ApplicationAnswerService,
    user_id: str,
) -> BaseTool:
    """Create an application drafting tool bound to a trusted user identity."""

    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    user_id = user_id.strip()
    if not user_id:
        raise ValueError("user_id must not be empty")

    async def generate_application_answer(
        question: str,
        job: JobDescription,
        max_words: int | None = None,
    ) -> dict[str, Any]:
        result = await service.generate_answer(
            ApplicationAnswerRequest(
                user_id=user_id,
                question=question,
                job=job,
                max_words=max_words,
                additional_instructions=None,
            )
        )
        return result.model_dump(mode="json")

    return StructuredTool.from_function(
        coroutine=generate_application_answer,
        name="generate_application_answer",
        description=(
            "Generate a grounded draft answer for an application question using the current "
            "user's verified career evidence. Returns the draft, supporting evidence, and any "
            "missing information. This tool does not submit applications and must not make "
            "unsupported factual declarations on the user's behalf."
        ),
        args_schema=ApplicationAnswerGenerationInput,
    )
