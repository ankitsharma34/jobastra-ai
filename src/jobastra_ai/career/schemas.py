from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class CareerSchema(BaseModel):
    """Base configuration shared by career profile schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SkillLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    SELF_EMPLOYED = "self_employed"


class Skill(CareerSchema):
    name: str = Field(min_length=1)
    level: SkillLevel | None = None
    years_of_experience: float | None = Field(default=None, ge=0)


class WorkExperience(CareerSchema):
    title: str = Field(min_length=1)
    company: str = Field(min_length=1)
    employment_type: EmploymentType | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    description: str | None = None
    achievements: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.is_current and self.end_date is not None:
            raise ValueError("Current work experience cannot have an end date")
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("Work experience end date cannot precede start date")
        return self


class Education(CareerSchema):
    institution: str = Field(min_length=1)
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("Education end date cannot precede start date")
        return self


class Certification(CareerSchema):
    name: str = Field(min_length=1)
    issuer: str | None = None
    issued_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = None
    credential_url: HttpUrl | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.issued_date and self.expiration_date and self.expiration_date < self.issued_date:
            raise ValueError("Certification expiration date cannot precede issue date")
        return self


class Project(CareerSchema):
    name: str = Field(min_length=1)
    description: str | None = None
    role: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    technologies: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    url: HttpUrl | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("Project end date cannot precede start date")
        return self


class CareerPreferences(CareerSchema):
    target_roles: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    preferred_employment_types: list[EmploymentType] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)
    remote_preferred: bool | None = None


class CareerProfileExtractionRequest(CareerSchema):
    """Source content used to extract a structured career profile."""

    resume_text: str = Field(min_length=1)
    additional_context: str | None = None


CareerProfileExtractionInput = CareerProfileExtractionRequest


class CareerProfile(CareerSchema):
    full_name: str | None = None
    headline: str | None = None
    summary: str | None = None
    location: str | None = None
    years_of_experience: float | None = Field(default=None, ge=0)
    skills: list[Skill] = Field(default_factory=list)
    work_experience: list[WorkExperience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    preferences: CareerPreferences = Field(default_factory=CareerPreferences)
