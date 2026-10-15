from jobastra_ai.llm.services import LLMService
from jobastra_ai.rag.prompts import build_career_rag_prompt
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.schemas import CareerRAGRequest, CareerRAGResponse

INSUFFICIENT_EVIDENCE_ANSWER = (
    "I don't have enough career evidence to answer that question."
)


class CareerRAGService:
    """Answer career questions using retrieved user-scoped evidence."""

    def __init__(
        self,
        retriever: CareerRetriever,
        llm_service: LLMService,
    ) -> None:
        self._retriever = retriever
        self._llm_service = llm_service

    async def answer(self, request: CareerRAGRequest) -> CareerRAGResponse:
        evidence = await self._retriever.retrieve(
            user_id=request.user_id,
            query=request.question,
            top_k=request.top_k,
        )
        if not evidence:
            return CareerRAGResponse(
                answer=INSUFFICIENT_EVIDENCE_ANSWER,
                sources=[],
                has_evidence=False,
            )

        llm_request = build_career_rag_prompt(request.question, evidence)
        llm_response = await self._llm_service.ainvoke(llm_request)
        return CareerRAGResponse(
            answer=llm_response.content,
            sources=evidence,
            has_evidence=True,
        )
