from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.schemas import BlastRadiusResponse, GraphSummary, SeedRequest
from app.services import twin_service

router = APIRouter(prefix="/twin", tags=["digital-twin"])


@router.post("/seed")
async def seed(request: SeedRequest):
    edges = [(e.source, e.source_type, e.target, e.target_type) for e in request.edges]
    count = twin_service.seed_topology(edges)
    return {"edges_created": count}


@router.get("/blast-radius/{asset}", response_model=BlastRadiusResponse)
async def blast_radius(asset: str, entrypoint: str = Query(default=None)):
    try:
        result = twin_service.compute_blast_radius(asset, entrypoint or settings.default_entrypoint)
    except twin_service.AssetNotFoundError:
        raise HTTPException(status_code=404, detail=f"Asset '{asset}' not found in digital twin")
    return result


@router.get("/graph", response_model=GraphSummary)
async def graph():
    return twin_service.get_graph_summary()
