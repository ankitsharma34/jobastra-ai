from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class JobSchema(BaseModel):
    """Base configuration shared by job schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class WorkMode(StrEnum):
    ON_SITE = "on_site"
    HYBRID = "hybrid"
    REMOTE = "remote"


class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class Seniority(StrEnum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


class JobDescription(JobSchema):
    """Structured facts extracted from a job description."""

    title: str | None = None
    company: str | None = None
    location: str | None = None
    work_mode: WorkMode | None = None
    employment_type: EmploymentType | None = None
    seniority: Seniority | None = None
    responsibilities: list[str] | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    experience_requirements: str | None = None
    education_requirements: str | None = None


class JobDescriptionExtractionRequest(JobSchema):
    """Source content used to extract a structured job description."""

    job_text: str = Field(min_length=1)
    additional_context: str | None = None
