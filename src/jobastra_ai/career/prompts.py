from jobastra_ai.career.schemas import CareerProfileExtractionRequest
from jobastra_ai.llm.schemas import LLMRequest
from jobastra_ai.prompts import PromptMessageTemplate, PromptTemplate

CAREER_PROFILE_EXTRACTION_PROMPT = PromptTemplate(
    name="career.profile_extraction",
    version="1",
    messages=(
        PromptMessageTemplate(
            role="system",
            template=(
                "Extract factual career information from the supplied content.\n\n"
                "Rules:\n"
                "- Perform extraction only. Do not evaluate, score, rank, or recommend.\n"
                "- Do not invent, assume, or infer missing information.\n"
                "- Normalize skill names while preserving their factual meaning.\n"
                "- Preserve important employment, education, project, and achievement details.\n"
                "- Represent missing information with null values or empty collections.\n"
                "- Return only the requested structured schema."
            ),
        ),
        PromptMessageTemplate(
            role="user",
            template=(
                "Resume or career source content:\n"
                "{resume_text}\n\n"
                "Additional context:\n"
                "{additional_context}"
            ),
        ),
    ),
)


def build_career_profile_extraction_request(
    extraction_input: CareerProfileExtractionRequest,
) -> LLMRequest:
    """Render the career profile extraction prompt as an LLM request."""

    return CAREER_PROFILE_EXTRACTION_PROMPT.render(
        resume_text=extraction_input.resume_text,
        additional_context=extraction_input.additional_context or "No additional context provided.",
    )
