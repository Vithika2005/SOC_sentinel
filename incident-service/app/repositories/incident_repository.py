import uuid
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Incident, IncidentStatus, RawEvent


class IncidentRepository:
    """Repository pattern for data access (your notes: #Repository Pattern for data access)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_event_by_hash(self, event_hash: str) -> RawEvent | None:
        result = await self.session.execute(select(RawEvent).where(RawEvent.event_hash == event_hash))
        return result.scalar_one_or_none()

    async def find_correlatable_incident(self, asset: str, window_minutes: int) -> Incident | None:
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        result = await self.session.execute(
            select(Incident)
            .where(
                Incident.asset == asset,
                Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.INVESTIGATING]),
                Incident.last_event_at >= cutoff,
            )
            .order_by(Incident.last_event_at.desc())
        )
        return result.scalars().first()

    async def create_incident(self, incident: Incident) -> Incident:
        self.session.add(incident)
        await self.session.flush()  # populates incident.id without a full commit
        return incident

    async def add_event(self, event: RawEvent) -> RawEvent:
        self.session.add(event)
        await self.session.flush()
        return event

    async def get_by_id(self, incident_id: uuid.UUID) -> Incident | None:
        result = await self.session.execute(select(Incident).where(Incident.id == incident_id))
        return result.scalar_one_or_none()

    async def list_incidents(self, status: str | None = None, limit: int = 50, offset: int = 0) -> list[Incident]:
        query = select(Incident).order_by(Incident.last_event_at.desc()).limit(limit).offset(offset)
        if status:
            query = query.where(Incident.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_incidents(
        self,
        since: datetime | None = None,
        status: str | None = None,
        severity: str | None = None,
    ) -> int:
        query = select(func.count(Incident.id))
        if since:
            query = query.where(Incident.created_at >= since)
        if status:
            query = query.where(Incident.status == status)
        if severity:
            query = query.where(Incident.severity == severity)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def commit(self) -> None:
        await self.session.commit()
