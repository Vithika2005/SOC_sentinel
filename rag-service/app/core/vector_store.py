"""Singleton Qdrant client, collection created on first use if missing."""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings


class QdrantSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = QdrantClient(url=settings.qdrant_url)
            cls._instance._ensure_collection()
        return cls._instance

    def _ensure_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if settings.qdrant_collection not in existing:
            self.client.create_collection(
                collection_name=settings.qdrant_collection,
                vectors_config=VectorParams(size=settings.embedding_dim, distance=Distance.COSINE),
            )


qdrant = QdrantSingleton()
