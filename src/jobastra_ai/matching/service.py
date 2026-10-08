from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.prompts import build_job_matching_request
from jobastra_ai.matching.schemas import JobMatchRequest, JobMatchResult


class JobMatchingService:
    """Evaluate a career profile against a structured job description."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def match(self, request: JobMatchRequest) -> JobMatchResult:
        llm_request = build_job_matching_request(request)
        return await self._llm_service.ainvoke_structured(
            llm_request,
            JobMatchResult,
        )
