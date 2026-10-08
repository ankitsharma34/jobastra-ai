from jobastra_ai.jobs.prompts import build_job_description_extraction_request
from jobastra_ai.jobs.schemas import JobDescription, JobDescriptionExtractionRequest
from jobastra_ai.llm.services import LLMService


class JobDescriptionService:
    """Extract structured facts from job description content."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def extract(
        self,
        request: JobDescriptionExtractionRequest,
    ) -> JobDescription:
        llm_request = build_job_description_extraction_request(request)
        return await self._llm_service.ainvoke_structured(
            llm_request,
            JobDescription,
        )
