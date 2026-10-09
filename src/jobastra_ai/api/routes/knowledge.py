from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.api.dependencies import get_career_knowledge_service
from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.knowledge.service import CareerKnowledgeService

router = APIRouter(prefix="/career/knowledge", tags=["career knowledge"])


class CareerKnowledgeIndexRequest(BaseModel):
    """Development-only request for manually indexing a career profile."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    user_id: str = Field(min_length=1)
    profile_id: str = Field(min_length=1)
    profile: CareerProfile


@router.post(
    "/index",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Index a career profile",
    description=(
        "Development-only manual indexing endpoint. Before public deployment, user identity "
        "must come from trusted authentication rather than the request body."
    ),
)
async def index_career_knowledge(
    request: CareerKnowledgeIndexRequest,
    service: Annotated[CareerKnowledgeService, Depends(get_career_knowledge_service)],
) -> None:
    await service.index_profile(
        user_id=request.user_id,
        profile_id=request.profile_id,
        profile=request.profile,
    )
