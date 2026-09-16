"""STEP 14 -- Risk Agent (real). Calls the Digital Twin service for a
blast-radius computation on the incident's asset: what else breaks if this
asset is isolated/contained, on top of raw severity.

Falls back to the old stub shape if the Digital Twin is unreachable, so the
pipeline never hard-fails just because Neo4j/digital-twin isn't up yet.
"""
import logging

import httpx

from app.config import settings
from app.graph.state import AgentState

logger = logging.getLogger("orchestrator.risk")

SEVERITY_SCORE = {"low": 1, "medium": 2, "high": 3, "critical": 4}


async def risk_agent(state: AgentState) -> AgentState:
    asset = state.get("asset", "")
    severity_score = SEVERITY_SCORE.get(state.get("severity", "low"), 1)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.digital_twin_url}/twin/blast-radius/{asset}",
                params={"entrypoint": settings.digital_twin_entrypoint},
            )
            if response.status_code == 404:
                # Asset isn't in the digital twin yet -- not an error, just
                # nothing to compute. Common early on, before the twin is
                # fully seeded with every asset.
                state["risk_assessment"] = {
                    "status": "unknown_asset",
                    "note": f"'{asset}' not found in the digital twin",
                    "severity_score": severity_score,
                    "blast_radius": "unknown",
                    "affected_services": [],
                }
            else:
                response.raise_for_status()
                twin_result = response.json()
                state["risk_assessment"] = {
                    "status": "ok",
                    "severity_score": severity_score,
                    "blast_radius": twin_result.get("affected_count", 0),
                    "affected_services": twin_result.get("affected_services", []),
                    "services_unreachable_if_isolated": twin_result.get("services_unreachable_if_isolated", []),
                }
    except Exception as exc:
        logger.warning("Digital Twin unreachable (%s) -- falling back to stub", exc)
        state["risk_assessment"] = {
            "status": "stub",
            "note": "Digital Twin unreachable -- see digital-twin/README.md",
            "severity_score": severity_score,
            "blast_radius": "unknown",
            "affected_services": [],
        }

    state.setdefault("trace", []).append("risk_agent")
    return state
