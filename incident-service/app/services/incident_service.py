"""
Core business logic for STEP 11:
  - Deduplicate events
  - Correlate events into existing incidents
  - Assign Incident ID
  - Persist to Postgres
"""

import hashlib
import json
import uuid
from datetime import datetime

from app.config import settings
from app.core.bloom_filter import BloomFilter
from app.db.models import Incident, IncidentSeverity, IncidentStatus, RawEvent
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import NormalizedEvent

_dedup_filter = BloomFilter(
    capacity=settings.bloom_filter_capacity,
    error_rate=settings.bloom_filter_error_rate,
)

SEVERITY_RANK = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}


def _event_hash(event: NormalizedEvent) -> str:
    payload = json.dumps(
        {
            "asset": event.asset,
            "source_type": event.source_type,
            "message": event.message,
            "raw": event.raw,
        },
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _generate_incident_ref() -> str:
    return f"INC-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


def _naive(dt: datetime | None) -> datetime:
    """
    Convert any datetime (UTC-aware or naive) into a naive UTC datetime.
    """
    if dt is None:
        return datetime.utcnow()

    if dt.tzinfo is not None:
        return dt.astimezone().replace(tzinfo=None)

    return dt


class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def process_event(self, event: NormalizedEvent):
        event_hash = _event_hash(event)

        # ---------- Deduplication ----------
        if _dedup_filter.might_contain(event_hash):
            existing = await self.repository.get_event_by_hash(event_hash)
            if existing:
                incident = await self.repository.get_by_id(existing.incident_id)
                return incident, False

        _dedup_filter.add(event_hash)

        # ---------- Correlation ----------
        incident = await self.repository.find_correlatable_incident(
            event.asset,
            settings.correlation_window_minutes,
        )

        is_new = incident is None

        now = datetime.utcnow()
        event_time = _naive(event.timestamp)

        if incident is None:

            incident = Incident(
                incident_ref=_generate_incident_ref(),
                asset=event.asset,
                source_type=event.source_type,
                status=IncidentStatus.OPEN,
                severity=IncidentSeverity(
                    event.severity
                    if event.severity in SEVERITY_RANK
                    else "low"
                ),
                event_count=1,
                summary=event.message,
                created_at=now,
                updated_at=now,
                last_event_at=event_time,
            )

            incident = await self.repository.create_incident(incident)

        else:

            if (
                SEVERITY_RANK.get(event.severity, 0)
                > SEVERITY_RANK.get(incident.severity.value, 0)
            ):
                incident.severity = IncidentSeverity(event.severity)

            incident.updated_at = now
            incident.last_event_at = event_time
            incident.event_count += 1

        raw_event = RawEvent(
            incident_id=incident.id,
            event_hash=event_hash,
            source_type=event.source_type,
            asset=event.asset,
            severity=event.severity,
            raw_payload=event.raw,
            received_at=now,
        )

        await self.repository.add_event(raw_event)
        await self.repository.commit()

        return incident, is_new