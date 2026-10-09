from datetime import date

from langchain_core.documents import Document

from jobastra_ai.career.schemas import CareerProfile


def build_career_documents(
    profile: CareerProfile,
    user_id: str,
    profile_id: str,
) -> list[Document]:
    """Convert a career profile into independently retrievable documents."""

    user_id = _validate_identifier(user_id, "user_id")
    profile_id = _validate_identifier(profile_id, "profile_id")

    documents: list[Document] = []
    summary = _build_summary_document(profile, user_id, profile_id)
    if summary is not None:
        documents.append(summary)

    for index, experience in enumerate(profile.work_experience, start=1):
        lines = [
            f"Employment: {experience.title} at {experience.company}",
            _label("Employment type", experience.employment_type),
            _label("Location", experience.location),
            _date_range(experience.start_date, experience.end_date, experience.is_current),
            _label("Description", experience.description),
            _list_label("Achievements", experience.achievements),
            _list_label("Skills", experience.skills),
        ]
        documents.append(
            _document(
                lines,
                user_id,
                profile_id,
                source_type="work_experience",
                source_id=f"work-experience-{index}",
            )
        )

    for index, project in enumerate(profile.projects, start=1):
        lines = [
            f"Project: {project.name}",
            _label("Role", project.role),
            _date_range(project.start_date, project.end_date),
            _label("Description", project.description),
            _list_label("Technologies", project.technologies),
            _list_label("Achievements", project.achievements),
            _label("URL", project.url),
        ]
        documents.append(
            _document(
                lines,
                user_id,
                profile_id,
                source_type="project",
                source_id=f"project-{index}",
            )
        )

    for index, education in enumerate(profile.education, start=1):
        qualification = " in ".join(
            part for part in (education.degree, education.field_of_study) if part
        )
        lines = [
            f"Education: {education.institution}",
            _label("Qualification", qualification),
            _date_range(education.start_date, education.end_date),
            _label("Description", education.description),
        ]
        documents.append(
            _document(
                lines,
                user_id,
                profile_id,
                source_type="education",
                source_id=f"education-{index}",
            )
        )

    for index, certification in enumerate(profile.certifications, start=1):
        lines = [
            f"Certification: {certification.name}",
            _label("Issuer", certification.issuer),
            _label("Issued", certification.issued_date),
            _label("Expires", certification.expiration_date),
            _label("Credential ID", certification.credential_id),
            _label("Credential URL", certification.credential_url),
        ]
        documents.append(
            _document(
                lines,
                user_id,
                profile_id,
                source_type="certification",
                source_id=f"certification-{index}",
            )
        )

    return documents


def _build_summary_document(
    profile: CareerProfile,
    user_id: str,
    profile_id: str,
) -> Document | None:
    skill_lines = []
    for skill in profile.skills:
        details: list[str] = []
        if skill.level is not None:
            details.append(skill.level.value)
        if skill.years_of_experience is not None:
            details.append(f"{skill.years_of_experience:g} years")
        skill_lines.append(f"{skill.name} ({', '.join(details)})" if details else skill.name)

    lines = [
        _label("Name", profile.full_name),
        _label("Headline", profile.headline),
        _label("Location", profile.location),
        _label("Years of experience", profile.years_of_experience),
        _label("Summary", profile.summary),
        _list_label("Skills", skill_lines),
    ]
    if not any(lines):
        return None
    return _document(
        lines,
        user_id,
        profile_id,
        source_type="summary",
        source_id="summary-1",
    )


def _document(
    lines: list[str | None],
    user_id: str,
    profile_id: str,
    *,
    source_type: str,
    source_id: str,
) -> Document:
    metadata = {
        "user_id": user_id,
        "source_type": source_type,
        "source_id": source_id,
        "profile_id": profile_id,
    }
    return Document(
        id=f"{user_id}:{profile_id}:{source_id}",
        page_content="\n".join(line for line in lines if line),
        metadata=metadata,
    )


def _validate_identifier(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value.strip()


def _label(label: str, value: object | None) -> str | None:
    return f"{label}: {value}" if value not in (None, "") else None


def _list_label(label: str, values: list[str]) -> str | None:
    return f"{label}: {', '.join(values)}" if values else None


def _date_range(
    start_date: date | None,
    end_date: date | None,
    is_current: bool = False,
) -> str | None:
    if not start_date and not end_date and not is_current:
        return None
    start = start_date.isoformat() if start_date else "Unknown"
    end = "Present" if is_current else end_date.isoformat() if end_date else "Unknown"
    return f"Dates: {start} to {end}"
