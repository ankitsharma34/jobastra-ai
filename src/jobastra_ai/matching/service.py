from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.prompts import build_job_matching_request
from jobastra_ai.matching.schemas import JobMatchRequest, JobMatchResult
from jobastra_ai.rag.retriever import CareerRetriever

MATCHING_EVIDENCE_TOP_K = 5


class JobMatchingService:
    """Evaluate a career profile against a structured job description."""

    def __init__(
        self,
        llm_service: LLMService,
        retriever: CareerRetriever,
    ) -> None:
        self._llm_service = llm_service
        self._retriever = retriever

    async def match(self, request: JobMatchRequest) -> JobMatchResult:
        evidence = await self._retriever.retrieve(
            user_id=request.user_id,
            query=request.job_description.model_dump_json(exclude_none=True),
            top_k=MATCHING_EVIDENCE_TOP_K,
        )
        llm_request = build_job_matching_request(request, evidence)
        return await self._llm_service.ainvoke_structured(
            llm_request,
            JobMatchResult,
        )
