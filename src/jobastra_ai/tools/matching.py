from typing import Any

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, ConfigDict

from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.jobs.schemas import JobDescription
from jobastra_ai.matching.schemas import JobMatchRequest
from jobastra_ai.matching.service import JobMatchingService


class JobMatchingInput(BaseModel):
    """Arguments available to the model when matching the current user to a job."""

    model_config = ConfigDict(extra="forbid")

    job: JobDescription


def create_job_matching_tool(
    service: JobMatchingService,
    user_id: str,
    career_profile: CareerProfile,
) -> BaseTool:
    """Create a job matching tool bound to a trusted user and career profile."""

    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    user_id = user_id.strip()
    if not user_id:
        raise ValueError("user_id must not be empty")

    async def match_job(job: JobDescription) -> dict[str, Any]:
        result = await service.match(
            JobMatchRequest(
                user_id=user_id,
                career_profile=career_profile,
                job_description=job,
            )
        )
        return result.model_dump(mode="json")

    return StructuredTool.from_function(
        coroutine=match_job,
        name="match_job",
        description=(
            "Compare the current user's verified career profile and evidence with a structured "
            "job description. Returns a match score, strengths, missing skills, gaps, reasoning, "
            "and supporting source references."
        ),
        args_schema=JobMatchingInput,
    )
