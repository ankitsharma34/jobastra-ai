from pydantic import BaseModel, ConfigDict, Field


class RAGSchema(BaseModel):
    """Base configuration shared by career RAG schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CareerRAGRequest(RAGSchema):
    user_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)


class CareerEvidence(RAGSchema):
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    content: str = Field(min_length=1)


class CareerRAGResponse(RAGSchema):
    answer: str = Field(min_length=1)
    sources: list[CareerEvidence]
    has_evidence: bool
