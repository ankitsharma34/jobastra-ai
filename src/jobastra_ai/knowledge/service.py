from jobastra_ai.career.schemas import CareerProfile
from jobastra_ai.knowledge.chunking import chunk_career_documents
from jobastra_ai.knowledge.documents import build_career_documents
from jobastra_ai.knowledge.store import CareerPGVector


class CareerKnowledgeService:
    """Index career profiles as user-scoped vector knowledge."""

    def __init__(self, vector_store: CareerPGVector) -> None:
        self._vector_store = vector_store

    async def index_profile(
        self,
        user_id: str,
        profile_id: str,
        profile: CareerProfile,
    ) -> None:
        documents = build_career_documents(profile, user_id, profile_id)
        chunks = chunk_career_documents(documents)

        normalized_user_id = user_id.strip()
        normalized_profile_id = profile_id.strip()
        await self._vector_store.adelete_by_metadata(
            {
                "user_id": normalized_user_id,
                "profile_id": normalized_profile_id,
            }
        )

        if chunks:
            await self._vector_store.aadd_documents(chunks)
