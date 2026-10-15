from jobastra_ai.llm.services import LLMService
from jobastra_ai.matching.prompts import build_job_matching_request
from jobastra_ai.matching.schemas import (
    JobMatchEvidenceReference,
    JobMatchRequest,
    JobMatchResult,
)
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.schemas import CareerEvidence

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
        result = await self._llm_service.ainvoke_structured(
            llm_request,
            JobMatchResult,
        )
        return result.model_copy(
            update={"evidence_references": self._validated_references(result, evidence)}
        )

    @staticmethod
    def _validated_references(
        result: JobMatchResult,
        evidence: list[CareerEvidence],
    ) -> list[JobMatchEvidenceReference]:
        allowed_source_ids = {item.source_id for item in evidence}
        matched_skills = {skill.casefold() for skill in result.matched_skills}
        strengths = {strength.casefold() for strength in result.strengths}
        references: list[JobMatchEvidenceReference] = []

        for reference in result.evidence_references:
            valid_claims = matched_skills if reference.category == "matched_skill" else strengths
            source_ids = list(
                dict.fromkeys(
                    source_id
                    for source_id in reference.source_ids
                    if source_id in allowed_source_ids
                )
            )
            if reference.claim.casefold() in valid_claims and source_ids:
                references.append(reference.model_copy(update={"source_ids": source_ids}))

        return references
