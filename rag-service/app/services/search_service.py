from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.config import settings
from app.core.embeddings import embedding_model
from app.core.vector_store import qdrant
from app.schemas import SearchHit


class SearchService:
    def search(self, query: str, top_k: int = 5, source_filter: str | None = None) -> list[SearchHit]:
        vector = embedding_model.embed_one(query)

        query_filter = None
        if source_filter:
            query_filter = Filter(must=[FieldCondition(key="source", match=MatchValue(value=source_filter))])

        response = qdrant.client.query_points(
            collection_name=settings.qdrant_collection,
            query=vector,
            limit=top_k,
            query_filter=query_filter,
        )
        results = response.points

        return [
            SearchHit(
                score=r.score,
                source=r.payload.get("source", "unknown"),
                title=r.payload.get("title", ""),
                text=r.payload.get("text", ""),
                metadata={k: v for k, v in r.payload.items() if k not in {"source", "title", "text"}},
            )
            for r in results
        ]


search_service = SearchService()
