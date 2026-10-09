from langchain_core.embeddings import Embeddings


class EmbeddingService:
    """Provide asynchronous access to a configured embedding model."""

    def __init__(self, model: Embeddings) -> None:
        self._model = model

    async def embed_query(self, text: str) -> list[float]:
        self._validate_text(text, name="text")
        return await self._model.aembed_query(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not isinstance(texts, list):
            raise TypeError("texts must be a list of strings")
        if not texts:
            raise ValueError("texts must contain at least one document")
        for index, text in enumerate(texts):
            self._validate_text(text, name=f"texts[{index}]")
        return await self._model.aembed_documents(texts)

    @staticmethod
    def _validate_text(text: object, *, name: str) -> None:
        if not isinstance(text, str):
            raise TypeError(f"{name} must be a string")
        if not text.strip():
            raise ValueError(f"{name} must not be empty")
