from collections.abc import Sequence

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100


def chunk_career_documents(
    documents: Sequence[Document],
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Document]:
    """Split long career documents while preserving source metadata."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be non-negative and smaller than chunk_size")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks: list[Document] = []

    for document in documents:
        parent_id = _get_parent_id(document)
        texts = (
            [document.page_content]
            if len(document.page_content) <= chunk_size
            else splitter.split_text(document.page_content)
        )
        chunk_count = len(texts)

        for index, text in enumerate(texts, start=1):
            chunk_id = f"{parent_id}:chunk-{index}"
            chunks.append(
                Document(
                    id=chunk_id,
                    page_content=text,
                    metadata={
                        **document.metadata,
                        "chunk_id": chunk_id,
                        "chunk_index": index,
                        "chunk_count": chunk_count,
                    },
                )
            )

    return chunks


def _get_parent_id(document: Document) -> str:
    if document.id:
        return document.id

    required_metadata = ("user_id", "profile_id", "source_id")
    if all(document.metadata.get(key) for key in required_metadata):
        return ":".join(str(document.metadata[key]) for key in required_metadata)

    raise ValueError("Each document must have an id or user_id, profile_id, and source_id metadata")
