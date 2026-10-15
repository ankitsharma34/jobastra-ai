from langchain_core.documents import Document

from jobastra_ai.knowledge.store import CareerPGVector
from jobastra_ai.rag.schemas import CareerEvidence


class CareerRetriever:
    """Retrieve user-scoped evidence from career knowledge."""

    def __init__(self, vector_store: CareerPGVector) -> None:
        self._vector_store = vector_store

    async def retrieve(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        *,
        profile_id: str | None = None,
    ) -> list[CareerEvidence]:
        user_id = self._validate_text(user_id, "user_id")
        query = self._validate_text(query, "query")
        if not 1 <= top_k <= 10:
            raise ValueError("top_k must be between 1 and 10")

        metadata_filter = {"user_id": user_id}
        if profile_id is not None:
            metadata_filter["profile_id"] = self._validate_text(
                profile_id,
                "profile_id",
            )

        documents = await self._vector_store.asimilarity_search(
            query,
            k=top_k,
            filter=metadata_filter,
        )
        return [self._to_evidence(document) for document in documents]

    @staticmethod
    def _to_evidence(document: Document) -> CareerEvidence:
        source_id = document.metadata.get("source_id")
        source_type = document.metadata.get("source_type")
        if not isinstance(source_id, str) or not isinstance(source_type, str):
            raise ValueError("Retrieved career document is missing source metadata")

        return CareerEvidence(
            source_id=source_id,
            source_type=source_type,
            content=document.page_content,
        )

    @staticmethod
    def _validate_text(value: object, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        if not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()
