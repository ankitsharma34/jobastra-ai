from typing import Annotated

from fastapi import APIRouter, Depends

from jobastra_ai.api.dependencies import get_job_description_service
from jobastra_ai.jobs.schemas import JobDescription, JobDescriptionExtractionRequest
from jobastra_ai.jobs.service import JobDescriptionService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/extract", response_model=JobDescription)
async def extract_job_description(
    request: JobDescriptionExtractionRequest,
    service: Annotated[JobDescriptionService, Depends(get_job_description_service)],
) -> JobDescription:
    return await service.extract(request)
