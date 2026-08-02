import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import IncidentStatus
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import DashboardStats, IncidentOut

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentOut])
async def list_incidents(
    status: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    session: AsyncSession = Depends(get_db),
):
    repository = IncidentRepository(session)
    return await repository.list_incidents(status=status, limit=limit, offset=offset)


@router.get("/dashboard/stats", response_model=DashboardStats)
async def dashboard_stats(session: AsyncSession = Depends(get_db)):
    repository = IncidentRepository(session)
    since_24h = datetime.utcnow() - timedelta(hours=24)
    return DashboardStats(
        total_incidents=await repository.count_incidents(),
        open_incidents=await repository.count_incidents(status=IncidentStatus.OPEN),
        critical_incidents=await repository.count_incidents(severity="critical"),
        incidents_last_24h=await repository.count_incidents(since=since_24h),
    )


@router.get("/{incident_id}", response_model=IncidentOut)
async def get_incident(incident_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    repository = IncidentRepository(session)
    incident = await repository.get_by_id(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("/{incident_id}/resolve", response_model=IncidentOut)
async def resolve_incident(incident_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    repository = IncidentRepository(session)
    incident = await repository.get_by_id(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = IncidentStatus.RESOLVED
    await repository.commit()
    return incident
