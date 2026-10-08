from typing import Annotated

from fastapi import APIRouter, Depends

from jobastra_ai.api.dependencies import get_job_matching_service
from jobastra_ai.matching.schemas import JobMatchRequest, JobMatchResult
from jobastra_ai.matching.service import JobMatchingService

router = APIRouter(prefix="/jobs", tags=["matching"])


@router.post("/match", response_model=JobMatchResult)
async def match_job(
    request: JobMatchRequest,
    service: Annotated[JobMatchingService, Depends(get_job_matching_service)],
) -> JobMatchResult:
    return await service.match(request)
