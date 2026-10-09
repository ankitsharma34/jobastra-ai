from typing import Annotated

from fastapi import Depends

from jobastra_ai.career.service import CareerProfileService
from jobastra_ai.jobs.service import JobDescriptionService
from jobastra_ai.knowledge.service import CareerKnowledgeService
from jobastra_ai.knowledge.store import CareerPGVector, get_vector_store
from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.service import JobMatchingService


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


def get_job_matching_service(
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> JobMatchingService:
    return JobMatchingService(llm_service)


def get_career_knowledge_service(
    vector_store: Annotated[CareerPGVector, Depends(get_vector_store)],
) -> CareerKnowledgeService:
    return CareerKnowledgeService(vector_store)
