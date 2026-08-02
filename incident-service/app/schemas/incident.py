import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class NormalizedEvent(BaseModel):
    """Shape your Normalizer's Kafka messages should already match (or map to)."""
    source_type: str          # e.g. "runtime", "appsec", "iac", "auth"
    asset: str                # e.g. "api-service", "10.0.1.5", "auth-container"
    severity: str = "low"     # low | medium | high | critical
    message: Optional[str] = None
    raw: dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[datetime] = None


class IncidentOut(BaseModel):
    id: uuid.UUID
    incident_ref: str
    asset: str
    source_type: str
    status: str
    severity: str
    event_count: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_event_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_incidents: int
    open_incidents: int
    critical_incidents: int
    incidents_last_24h: int
