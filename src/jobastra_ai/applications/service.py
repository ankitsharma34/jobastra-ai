from jobastra_ai.applications.schemas import ApplicationAnswerRequest
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.schemas import CareerEvidence

APPLICATION_EVIDENCE_TOP_K = 5


class ApplicationAnswerService:
    """Retrieve user-scoped career evidence for application answers."""

    def __init__(self, retriever: CareerRetriever) -> None:
        self._retriever = retriever

    async def retrieve_evidence(
        self,
        request: ApplicationAnswerRequest,
    ) -> list[CareerEvidence]:
        query = (
            f"Application question: {request.question}\n"
            "Target job requirements: "
            f"{request.job.model_dump_json(exclude_none=True)}"
        )
        return await self._retriever.retrieve(
            user_id=request.user_id,
            query=query,
            top_k=APPLICATION_EVIDENCE_TOP_K,
        )
