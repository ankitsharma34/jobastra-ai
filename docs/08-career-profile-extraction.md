# Career profile extraction

## Purpose and flow

```mermaid
flowchart LR
    PDF[Uploaded PDF] --> Validate[Type/size validation]
    Validate --> Parse[pypdf extract_text]
    Parse --> Input[CareerProfileExtractionRequest]
    Input --> Prompt[Extraction prompt]
    Prompt --> LLM[LLMService structured call]
    LLM --> Profile[CareerProfile]
```

`api/routes/career.py` accepts `application/pdf` or `application/x-pdf`, reads at most 10 MB + 1 byte, and offloads synchronous parsing to a thread pool. `documents/pdf.py` rejects encrypted, unreadable, empty-text, and scanned-only documents. `career/service.py` renders `CAREER_PROFILE_EXTRACTION_PROMPT` and asks `LLMService.ainvoke_structured` for `CareerProfile`.

The prompt explicitly performs extraction rather than evaluation, normalizes skill names, preserves important details, and uses null/empty values for missing facts. Pydantic schemas in `career/schemas.py` represent skills, work, projects, education, certifications, and preferences. Cross-field validators prevent reversed dates and current employment with an end date.

## Example output

```json
{
  "full_name": "A Candidate",
  "headline": "Backend Engineer",
  "skills": [{"name":"Python","level":null,"years_of_experience":null}],
  "work_experience": [], "projects": [], "education": [], "certifications": [],
  "preferences": {"target_roles":[],"preferred_locations":[],"preferred_employment_types":[],"industries":[],"remote_preferred":null}
}
```

Extraction accuracy is provider-dependent. No page/count limit beyond bytes, OCR, malware scanning, contact-data redaction, confidence score, or human correction workflow exists. Schema validation proves structural validity, while factual accuracy still requires source review.
