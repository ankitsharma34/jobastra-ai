from jobastra_ai.career.prompts import build_career_profile_extraction_request
from jobastra_ai.career.schemas import CareerProfile, CareerProfileExtractionRequest
from jobastra_ai.llm.services import LLMService


class CareerProfileService:
    """Extract structured career profiles from source content."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def extract_profile(
        self,
        request: CareerProfileExtractionRequest,
    ) -> CareerProfile:
        llm_request = build_career_profile_extraction_request(request)
        return await self._llm_service.ainvoke_structured(
            llm_request,
            CareerProfile,
        )
