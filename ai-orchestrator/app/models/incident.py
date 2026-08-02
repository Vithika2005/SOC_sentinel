from pydantic import BaseModel


class Incident(BaseModel):
    incident_id: str
    asset: str
    severity: str
    summary: str