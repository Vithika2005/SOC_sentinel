import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IncidentRecord(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_ref = Column(String(64), unique=True, index=True, nullable=False)
    asset = Column(String(128), nullable=False)
    source_type = Column(String(64), nullable=False)
    severity = Column(String(32), nullable=False)
    summary = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Complete multi-agent pipeline payload stored as structured JSON
    recon_findings = Column(JSON, nullable=True)
    threat_intel = Column(JSON, nullable=True)
    risk_assessment = Column(JSON, nullable=True)
    decision = Column(JSON, nullable=True)
    audit = Column(JSON, nullable=True)
    trace = Column(JSON, nullable=True)