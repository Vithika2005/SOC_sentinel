from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Incident(BaseModel):
    """
    Represents the incident payload received from the
    Incident Service (Milestone 4).
    """

    id: Optional[str] = None
    incident_ref: str
    asset: str
    source_type: str
    status: str
    severity: str
    event_count: int
    summary: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_event_at: Optional[datetime] = None

    is_new: Optional[bool] = None