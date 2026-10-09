from datetime import date

from langchain_core.documents import Document

from jobastra_ai.career.schemas import CareerProfile


def build_career_documents(profile: CareerProfile, user_id: str) -> list[Document]:
    """Convert a career profile into independently retrievable documents."""

    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    if not user_id.strip():
        raise ValueError("user_id must not be empty")
    user_id = user_id.strip()

    documents: list[Document] = []
    summary = _build_summary_document(profile, user_id)
    if summary is not None:
        documents.append(summary)

    for index, experience in enumerate(profile.work_experience):
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
            _document(lines, user_id, section="work_experience", index=index)
        )

    for index, project in enumerate(profile.projects):
        lines = [
            f"Project: {project.name}",
            _label("Role", project.role),
            _date_range(project.start_date, project.end_date),
            _label("Description", project.description),
            _list_label("Technologies", project.technologies),
            _list_label("Achievements", project.achievements),
            _label("URL", project.url),
        ]
        documents.append(_document(lines, user_id, section="project", index=index))

    for index, education in enumerate(profile.education):
        qualification = " in ".join(
            part for part in (education.degree, education.field_of_study) if part
        )
        lines = [
            f"Education: {education.institution}",
            _label("Qualification", qualification),
            _date_range(education.start_date, education.end_date),
            _label("Description", education.description),
        ]
        documents.append(_document(lines, user_id, section="education", index=index))

    for index, certification in enumerate(profile.certifications):
        lines = [
            f"Certification: {certification.name}",
            _label("Issuer", certification.issuer),
            _label("Issued", certification.issued_date),
            _label("Expires", certification.expiration_date),
            _label("Credential ID", certification.credential_id),
            _label("Credential URL", certification.credential_url),
        ]
        documents.append(_document(lines, user_id, section="certification", index=index))

    return documents


def _build_summary_document(profile: CareerProfile, user_id: str) -> Document | None:
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
    return _document(lines, user_id, section="summary")


def _document(
    lines: list[str | None],
    user_id: str,
    *,
    section: str,
    index: int | None = None,
) -> Document:
    metadata: dict[str, str | int] = {
        "user_id": user_id,
        "source": "career_profile",
        "section": section,
    }
    if index is not None:
        metadata["index"] = index
    return Document(
        page_content="\n".join(line for line in lines if line),
        metadata=metadata,
    )


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
