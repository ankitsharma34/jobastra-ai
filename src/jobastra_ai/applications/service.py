from jobastra_ai.applications.prompts import build_application_answer_prompt
from jobastra_ai.applications.schemas import (
    ApplicationAnswerRequest,
    ApplicationAnswerResponse,
)
from jobastra_ai.llm.services import LLMService
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.rag.schemas import CareerEvidence

APPLICATION_EVIDENCE_TOP_K = 5
NO_EVIDENCE_MESSAGE = "Verified career evidence relevant to this application question"
SENSITIVE_INFORMATION_RULES = (
    (
        "Work authorization, visa, sponsorship, or legal work eligibility",
        (
            "authorized to work",
            "work authorization",
            "visa status",
            "visa sponsorship",
            "require sponsorship",
            "legal eligibility",
            "legally eligible",
        ),
    ),
    (
        "Criminal, legal, or background history",
        (
            "criminal history",
            "criminal record",
            "conviction",
            "background history",
            "background check",
        ),
    ),
)


class ApplicationAnswerService:
    """Retrieve user-scoped career evidence for application answers."""

    def __init__(
        self,
        retriever: CareerRetriever,
        llm_service: LLMService,
    ) -> None:
        self._retriever = retriever
        self._llm_service = llm_service

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

    async def generate_answer(
        self,
        request: ApplicationAnswerRequest,
    ) -> ApplicationAnswerResponse:
        evidence = await self.retrieve_evidence(request)
        if not evidence:
            return self._needs_user_input([NO_EVIDENCE_MESSAGE])

        missing_sensitive_information = self._missing_sensitive_information(
            request.question,
            evidence,
        )
        if missing_sensitive_information:
            return self._needs_user_input(missing_sensitive_information)

        llm_request = build_application_answer_prompt(request, evidence)
        result = await self._llm_service.ainvoke_structured(
            llm_request,
            ApplicationAnswerResponse,
        )
        needs_user_input = result.needs_user_input or result.answer is None
        missing_information = result.missing_information
        if needs_user_input and not missing_information:
            missing_information = [NO_EVIDENCE_MESSAGE]
        elif not needs_user_input:
            missing_information = []

        return ApplicationAnswerResponse(
            answer=result.answer,
            sources=self._validated_sources(result.sources, evidence),
            needs_user_input=needs_user_input,
            missing_information=missing_information,
        )

    @staticmethod
    def _missing_sensitive_information(
        question: str,
        evidence: list[CareerEvidence],
    ) -> list[str]:
        normalized_question = question.casefold()
        normalized_evidence = "\n".join(item.content for item in evidence).casefold()
        return [
            description
            for description, terms in SENSITIVE_INFORMATION_RULES
            if any(term in normalized_question for term in terms)
            and not any(term in normalized_evidence for term in terms)
        ]

    @staticmethod
    def _validated_sources(
        sources: list[CareerEvidence],
        evidence: list[CareerEvidence],
    ) -> list[CareerEvidence]:
        retrieved_sources = {(item.source_type, item.source_id): item for item in evidence}
        validated_sources: list[CareerEvidence] = []
        seen: set[tuple[str, str]] = set()
        for source in sources:
            key = (source.source_type, source.source_id)
            if key in retrieved_sources and key not in seen:
                validated_sources.append(retrieved_sources[key])
                seen.add(key)
        return validated_sources

    @staticmethod
    def _needs_user_input(
        missing_information: list[str],
    ) -> ApplicationAnswerResponse:
        return ApplicationAnswerResponse(
            answer=None,
            sources=[],
            needs_user_input=True,
            missing_information=missing_information,
        )
