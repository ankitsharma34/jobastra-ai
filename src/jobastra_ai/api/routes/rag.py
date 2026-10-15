from typing import Annotated

from fastapi import APIRouter, Depends

from jobastra_ai.api.dependencies import get_career_rag_service
from jobastra_ai.rag.schemas import CareerRAGRequest, CareerRAGResponse
from jobastra_ai.rag.service import CareerRAGService

router = APIRouter(prefix="/career/rag", tags=["career RAG"])


@router.post(
    "/answer",
    response_model=CareerRAGResponse,
    summary="Answer a question using career evidence",
    description=(
        "For development, user_id is accepted in the request body. Before public deployment, "
        "it must be resolved from trusted authentication."
    ),
)
async def answer_career_question(
    request: CareerRAGRequest,
    service: Annotated[CareerRAGService, Depends(get_career_rag_service)],
) -> CareerRAGResponse:
    return await service.answer(request)
