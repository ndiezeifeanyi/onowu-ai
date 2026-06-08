from abc import ABC, abstractmethod
from typing import Any

from app.core.config import get_settings


class VectorProvider(ABC):
    @abstractmethod
    async def upsert(self, *, user_id: str, item_id: str, text: str, metadata: dict[str, Any]) -> str:
        """Store a memory vector and return an embedding id."""

    @abstractmethod
    async def search(self, *, user_id: str, query: str, limit: int) -> list[dict[str, Any]]:
        """Search user-scoped vector memory."""


class InMemoryVectorProvider(VectorProvider):
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []

    async def upsert(self, *, user_id: str, item_id: str, text: str, metadata: dict[str, Any]) -> str:
        embedding_id = f"local-{item_id}"
        self._items.append(
            {"user_id": user_id, "item_id": item_id, "text": text, "metadata": metadata, "id": embedding_id}
        )
        return embedding_id

    async def search(self, *, user_id: str, query: str, limit: int) -> list[dict[str, Any]]:
        words = set(query.lower().split())
        matches = []
        for item in self._items:
            if item["user_id"] != user_id:
                continue
            score = len(words.intersection(item["text"].lower().split()))
            if score:
                matches.append({**item, "score": score})
        return sorted(matches, key=lambda row: row["score"], reverse=True)[:limit]


class ChromaVectorProvider(VectorProvider):
    async def upsert(self, *, user_id: str, item_id: str, text: str, metadata: dict[str, Any]) -> str:
        try:
            import chromadb
        except ImportError:
            return await InMemoryVectorProvider().upsert(
                user_id=user_id, item_id=item_id, text=text, metadata=metadata
            )
        settings = get_settings()
        client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        collection = client.get_or_create_collection("personal_ai_os_memory")
        embedding_id = f"{user_id}:{item_id}"
        collection.upsert(
            ids=[embedding_id],
            documents=[text],
            metadatas=[{"user_id": user_id, **metadata}],
        )
        return embedding_id

    async def search(self, *, user_id: str, query: str, limit: int) -> list[dict[str, Any]]:
        try:
            import chromadb
        except ImportError:
            return []
        settings = get_settings()
        client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        collection = client.get_or_create_collection("personal_ai_os_memory")
        result = collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id},
        )
        rows = []
        for idx, item_id in enumerate(result.get("ids", [[]])[0]):
            rows.append(
                {
                    "id": item_id,
                    "text": result.get("documents", [[]])[0][idx],
                    "metadata": result.get("metadatas", [[]])[0][idx],
                    "distance": result.get("distances", [[]])[0][idx]
                    if result.get("distances")
                    else None,
                }
            )
        return rows


class PineconeVectorProvider(VectorProvider):
    async def upsert(self, *, user_id: str, item_id: str, text: str, metadata: dict[str, Any]) -> str:
        raise NotImplementedError("Pinecone adapter requires an embedding provider configuration.")

    async def search(self, *, user_id: str, query: str, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Pinecone adapter requires an embedding provider configuration.")


def build_vector_provider() -> VectorProvider:
    settings = get_settings()
    if settings.vector_provider.lower() == "pinecone":
        return PineconeVectorProvider()
    if settings.vector_provider.lower() == "memory":
        return InMemoryVectorProvider()
    return ChromaVectorProvider()

