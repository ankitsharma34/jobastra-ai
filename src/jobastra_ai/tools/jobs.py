from typing import Any

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.jobs.schemas import JobDescriptionExtractionRequest
from jobastra_ai.jobs.service import JobDescriptionService


class JobDescriptionAnalysisInput(BaseModel):
    """Arguments available to the model when analyzing a job description."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    job_text: str = Field(min_length=1)


def create_job_description_analysis_tool(
    service: JobDescriptionService,
) -> BaseTool:
    """Create a tool backed by the existing job description service."""

    async def analyze_job_description(job_text: str) -> dict[str, Any]:
        job = await service.extract(JobDescriptionExtractionRequest(job_text=job_text))
        return job.model_dump(mode="json")

    return StructuredTool.from_function(
        coroutine=analyze_job_description,
        name="analyze_job_description",
        description=("Extract factual, structured job requirements from raw job description text."),
        args_schema=JobDescriptionAnalysisInput,
    )
