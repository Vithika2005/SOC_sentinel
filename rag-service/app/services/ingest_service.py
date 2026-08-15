import uuid

from qdrant_client.models import PointStruct

from app.config import settings
from app.core.embeddings import embedding_model
from app.core.vector_store import qdrant


def ingest_documents(documents: list[dict]) -> int:
    """documents: [{"source": "mitre", "title": "...", "text": "...", "metadata": {...}}]"""
    if not documents:
        return 0

    texts = [d["text"] for d in documents]
    vectors = embedding_model.embed(texts)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "source": doc["source"],
                "title": doc["title"],
                "text": doc["text"],
                **doc.get("metadata", {}),
            },
        )
        for doc, vector in zip(documents, vectors)
    ]

    qdrant.client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)
