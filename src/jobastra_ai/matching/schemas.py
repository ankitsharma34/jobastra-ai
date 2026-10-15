from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.jobs.schemas import JobDescription


class MatchingSchema(BaseModel):
    """Base configuration shared by job matching schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class JobMatchRequest(MatchingSchema):
    user_id: str = Field(min_length=1)
    career_profile: CareerProfile
    job_description: JobDescription


class JobMatchEvidenceReference(MatchingSchema):
    category: Literal["matched_skill", "strength"]
    claim: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)


class JobMatchResult(MatchingSchema):
    match_score: int = Field(ge=0, le=100)
    recommendation: Literal["strong_match", "potential_match", "weak_match"]
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    gaps: list[str]
    reasoning: str = Field(min_length=1)
    evidence_references: list[JobMatchEvidenceReference] = Field(default_factory=list)
