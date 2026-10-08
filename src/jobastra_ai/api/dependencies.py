from typing import Annotated

from fastapi import Depends

from jobastra_ai.career.service import CareerProfileService
from jobastra_ai.jobs.service import JobDescriptionService
from jobastra_ai.llm.services import LLMService


def get_llm_service() -> LLMService:
    return LLMService()


def get_career_profile_service(
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> CareerProfileService:
    return CareerProfileService(llm_service)


def get_job_description_service(
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> JobDescriptionService:
    return JobDescriptionService(llm_service)
