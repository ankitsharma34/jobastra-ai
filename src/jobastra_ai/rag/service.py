import re

from jobastra_ai.llm.services import LLMService
from jobastra_ai.rag.prompts import build_career_rag_prompt
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.schemas import CareerEvidence, CareerRAGRequest, CareerRAGResponse

INSUFFICIENT_EVIDENCE_ANSWER = "I don't have enough career evidence to answer that question."
SOURCE_REFERENCE_PATTERN = re.compile(r"\[([A-Za-z0-9][A-Za-z0-9._:-]*)\]")


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
        retrieved_evidence = await self._retriever.retrieve(
            user_id=request.user_id,
            query=request.question,
            top_k=request.top_k,
        )
        if not retrieved_evidence:
            return CareerRAGResponse(
                answer=INSUFFICIENT_EVIDENCE_ANSWER,
                sources=[],
                has_evidence=False,
            )

        evidence = self._merge_sources(retrieved_evidence)
        llm_request = build_career_rag_prompt(request.question, evidence)
        llm_response = await self._llm_service.ainvoke(llm_request)
        return CareerRAGResponse(
            answer=self._remove_unknown_source_references(
                llm_response.content,
                evidence,
            ),
            sources=evidence,
            has_evidence=True,
        )

    @staticmethod
    def _merge_sources(evidence: list[CareerEvidence]) -> list[CareerEvidence]:
        merged: dict[tuple[str, str], CareerEvidence] = {}
        for item in evidence:
            key = (item.source_type, item.source_id)
            existing = merged.get(key)
            if existing is None:
                merged[key] = item
            elif item.content in existing.content:
                continue
            elif existing.content in item.content:
                merged[key] = item
            else:
                merged[key] = existing.model_copy(
                    update={"content": f"{existing.content}\n\n{item.content}"}
                )
        return list(merged.values())

    @staticmethod
    def _remove_unknown_source_references(
        answer: str,
        evidence: list[CareerEvidence],
    ) -> str:
        allowed_source_ids = {item.source_id for item in evidence}

        def replace_reference(match: re.Match[str]) -> str:
            return match.group(0) if match.group(1) in allowed_source_ids else ""

        sanitized_answer = SOURCE_REFERENCE_PATTERN.sub(replace_reference, answer).strip()
        return sanitized_answer or INSUFFICIENT_EVIDENCE_ANSWER
