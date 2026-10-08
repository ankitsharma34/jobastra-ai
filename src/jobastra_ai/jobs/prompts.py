from jobastra_ai.jobs.schemas import JobDescriptionExtractionRequest
from jobastra_ai.llm.schemas import LLMRequest
from jobastra_ai.prompts import PromptMessageTemplate, PromptTemplate

JOB_DESCRIPTION_EXTRACTION_PROMPT = PromptTemplate(
    name="jobs.description_extraction",
    version="1",
    messages=(
        PromptMessageTemplate(
            role="system",
            template=(
                "Extract factual information from the supplied job description.\n\n"
                "Rules:\n"
                "- Extract only information explicitly stated in the source content.\n"
                "- Do not invent, assume, or infer unstated requirements.\n"
                "- Normalize technology and skill names to their conventional names without "
                "changing their meaning.\n"
                "- Keep mandatory qualifications separate from preferred qualifications.\n"
                "- Preserve important responsibilities, experience requirements, and education "
                "requirements.\n"
                "- Treat absent information as unknown and represent it with null.\n"
                "- Apply the same extraction rules regardless of job category or industry.\n"
                "- Return only the requested structured schema."
            ),
        ),
        PromptMessageTemplate(
            role="user",
            template=("Job description:\n{job_text}\n\nAdditional context:\n{additional_context}"),
        ),
    ),
)


def build_job_description_extraction_request(
    extraction_request: JobDescriptionExtractionRequest,
) -> LLMRequest:
    """Render the job description extraction prompt as an LLM request."""

    return JOB_DESCRIPTION_EXTRACTION_PROMPT.render(
        job_text=extraction_request.job_text,
        additional_context=extraction_request.additional_context
        or "No additional context provided.",
    )
