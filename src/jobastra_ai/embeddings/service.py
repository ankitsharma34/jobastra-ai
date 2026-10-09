from langchain_core.embeddings import Embeddings


class EmbeddingService:
    """Provide asynchronous access to a configured embedding model."""

    def __init__(self, model: Embeddings) -> None:
        self._model = model

    async def embed_query(self, text: str) -> list[float]:
        return await self._model.aembed_query(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._model.aembed_documents(texts)
