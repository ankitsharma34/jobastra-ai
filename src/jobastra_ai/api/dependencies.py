from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from jobastra_ai.applications.service import ApplicationAnswerService
from jobastra_ai.career.service import CareerProfileService
from jobastra_ai.jobs.service import JobDescriptionService
from jobastra_ai.knowledge.service import CareerKnowledgeService
from jobastra_ai.knowledge.store import CareerPGVector, get_vector_store
from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.service import JobMatchingService
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.service import CareerRAGService


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


def get_career_knowledge_service(
    vector_store: Annotated[CareerPGVector, Depends(get_vector_store)],
) -> CareerKnowledgeService:
    return CareerKnowledgeService(vector_store)


def get_career_retriever(
    vector_store: Annotated[CareerPGVector, Depends(get_vector_store)],
) -> CareerRetriever:
    return CareerRetriever(vector_store)


def get_job_matching_service(
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
    retriever: Annotated[CareerRetriever, Depends(get_career_retriever)],
) -> JobMatchingService:
    return JobMatchingService(llm_service, retriever)


def get_career_rag_service(
    retriever: Annotated[CareerRetriever, Depends(get_career_retriever)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> CareerRAGService:
    return CareerRAGService(retriever, llm_service)


def get_application_answer_service(
    retriever: Annotated[CareerRetriever, Depends(get_career_retriever)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> ApplicationAnswerService:
    return ApplicationAnswerService(retriever, llm_service)


def get_authenticated_user_id(request: Request) -> str:
    """Return the user identity populated by trusted authentication middleware."""

    user_id = getattr(request.state, "user_id", None)
    if not isinstance(user_id, str) or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required",
        )
    return user_id.strip()
