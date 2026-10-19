from langchain_core.tools import BaseTool

from jobastra_ai.applications.service import ApplicationAnswerService
from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.jobs.service import JobDescriptionService
from jobastra_ai.matching.service import JobMatchingService
from jobastra_ai.rag.retriever import CareerRetriever
from jobastra_ai.tools.applications import create_application_answer_tool
from jobastra_ai.tools.career import create_career_evidence_tool
from jobastra_ai.tools.jobs import create_job_description_analysis_tool
from jobastra_ai.tools.matching import create_job_matching_tool


def create_agent_tools(
    user_id: str,
    career_profile: CareerProfile,
    career_retriever: CareerRetriever,
    job_service: JobDescriptionService,
    matching_service: JobMatchingService,
    application_service: ApplicationAnswerService,
) -> list[BaseTool]:
    """Create JobAstra tools bound to trusted user context and services."""

    return [
        create_career_evidence_tool(career_retriever, user_id),
        create_job_description_analysis_tool(job_service),
        create_job_matching_tool(matching_service, user_id, career_profile),
        create_application_answer_tool(application_service, user_id),
    ]
