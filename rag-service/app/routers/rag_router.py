from fastapi import APIRouter

from app.config import settings
from app.core.vector_store import qdrant
from app.schemas import IngestRequest, SearchRequest, SearchResponse
from app.services.ingest_service import ingest_documents
from app.services.search_service import search_service

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    hits = search_service.search(request.query, request.top_k, request.source_filter)
    return SearchResponse(query=request.query, hits=hits)


@router.post("/ingest")
async def ingest(request: IngestRequest):
    """Ad-hoc ingest endpoint -- the bulk loaders live in scripts/, this is
    for adding one-off documents (e.g. a new internal policy) without
    re-running a full script."""
    count = ingest_documents([doc.model_dump() for doc in request.documents])
    return {"ingested": count}


@router.get("/stats")
async def stats():
    info = qdrant.client.get_collection(settings.qdrant_collection)
    return {"collection": settings.qdrant_collection, "points_count": info.points_count}
