from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool

from jobastra_ai.api.dependencies import get_career_profile_service
from jobastra_ai.career.schemas import CareerProfile, CareerProfileExtractionRequest
from jobastra_ai.career.service import CareerProfileService
from jobastra_ai.documents import extract_text

router = APIRouter(prefix="/career", tags=["career"])

MAX_RESUME_SIZE_BYTES = 10 * 1024 * 1024
PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf"}


async def read_pdf_upload(resume: UploadFile) -> bytes:
    if resume.content_type not in PDF_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF resumes are supported",
        )

    content = await resume.read(MAX_RESUME_SIZE_BYTES + 1)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="The uploaded PDF is empty",
        )
    if len(content) > MAX_RESUME_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="The uploaded PDF exceeds the 10 MB size limit",
        )
    return content


@router.post("/profile/extract", response_model=CareerProfile)
async def extract_career_profile(
    resume: Annotated[UploadFile, File(description="PDF resume")],
    service: Annotated[CareerProfileService, Depends(get_career_profile_service)],
) -> CareerProfile:
    pdf_bytes = await read_pdf_upload(resume)
    resume_text = await run_in_threadpool(extract_text, pdf_bytes)
    request = CareerProfileExtractionRequest(resume_text=resume_text)
    return await service.extract_profile(request)
