from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.api.dependencies import (
    get_application_answer_service,
    get_authenticated_user_id,
)
from jobastra_ai.applications.schemas import (
    ApplicationAnswerRequest,
    ApplicationAnswerResponse,
)
from jobastra_ai.applications.service import ApplicationAnswerService
from jobastra_ai.jobs.schemas import JobDescription

router = APIRouter(prefix="/applications", tags=["applications"])


class ApplicationAnswerPayload(BaseModel):
    """Public payload whose user identity comes from authentication context."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    question: str = Field(min_length=1)
    job: JobDescription
    max_words: int | None = Field(default=None, ge=10, le=1000)
    additional_instructions: str | None = Field(default=None, min_length=1)


@router.post("/answer", response_model=ApplicationAnswerResponse)
async def generate_application_answer(
    payload: ApplicationAnswerPayload,
    user_id: Annotated[str, Depends(get_authenticated_user_id)],
    service: Annotated[ApplicationAnswerService, Depends(get_application_answer_service)],
) -> ApplicationAnswerResponse:
    request = ApplicationAnswerRequest(
        user_id=user_id,
        question=payload.question,
        job=payload.job,
        max_words=payload.max_words,
        additional_instructions=payload.additional_instructions,
    )
    return await service.generate_answer(request)
