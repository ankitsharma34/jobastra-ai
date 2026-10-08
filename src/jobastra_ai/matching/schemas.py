from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.jobs.schemas import JobDescription


class MatchingSchema(BaseModel):
    """Base configuration shared by job matching schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class JobMatchRequest(MatchingSchema):
    career_profile: CareerProfile
    job_description: JobDescription


class JobMatchResult(MatchingSchema):
    match_score: int = Field(ge=0, le=100)
    recommendation: Literal["strong_match", "potential_match", "weak_match"]
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    gaps: list[str]
    reasoning: str = Field(min_length=1)
