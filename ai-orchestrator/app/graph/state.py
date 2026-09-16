# ai-orchestrator/app/graph/state.py
"""
Shared state threaded through every node in the LangGraph pipeline:

    Incident -> Recon -> Threat Intel -> Risk -> Decision -> Auditor
"""

from typing_extensions import TypedDict, Optional
# ✅ app/graph/state.py - CORRECT
from typing_extensions import TypedDict

class AgentState(TypedDict, total=False):
    # Seeded from the Incident Service's Kafka payload
    incident_id: str
    incident_ref: str
    asset: str
    source_type: str
    severity: str
    summary: Optional[str]
    event_count: int

    # Populated by each agent as it runs
    recon_findings: dict
    threat_intel: dict
    risk_assessment: dict
    decision: dict
    audit: dict

    # Which agents actually ran, in order -- useful for debugging/observability
    trace: list[str]
