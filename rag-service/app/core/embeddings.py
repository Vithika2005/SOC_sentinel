"""Singleton embedding model (your notes: Singleton -> DB conn, Redis client,
Qdrant client -- the embedding model belongs in the same category: expensive
to load, should exist exactly once per process)."""
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer(settings.embedding_model)
        return cls._instance

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


embedding_model = EmbeddingModel()
