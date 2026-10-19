from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, ConfigDict, Field

from jobastra_ai.rag.retriever import CareerRetriever


class CareerEvidenceSearchInput(BaseModel):
    """Arguments available to the model when searching career evidence."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)


def create_career_evidence_tool(
    retriever: CareerRetriever,
    user_id: str,
) -> BaseTool:
    """Create a career search tool bound to a trusted user identity."""

    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    user_id = user_id.strip()
    if not user_id:
        raise ValueError("user_id must not be empty")

    async def search_career_evidence(
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, str]]:
        evidence = await retriever.retrieve(
            user_id=user_id,
            query=query,
            top_k=top_k,
        )
        return [item.model_dump(mode="json") for item in evidence]

    return StructuredTool.from_function(
        coroutine=search_career_evidence,
        name="search_career_evidence",
        description=(
            "Search the current user's verified career evidence for facts relevant to a query. "
            "Returns source identifiers, source types, and supporting content."
        ),
        args_schema=CareerEvidenceSearchInput,
    )
