# ai-orchestrator/app/graph/nodes/threat_intel.py
"""STEP 13 -- Threat Intel Agent (real). Calls the RAG service (Qdrant-backed)
for MITRE ATT&CK / OWASP / internal playbook matches against the incident context.
"""
import logging

import httpx

from app.config import settings
from app.graph.state import AgentState

logger = logging.getLogger("orchestrator.threat_intel")


async def threat_intel_agent(state: AgentState) -> AgentState:
    recon = state.get("recon_findings") or {}
    
    # Extract substantive incident attributes rather than agent meta-instructions
    summary = state.get("summary") or ""
    hypothesis = recon.get("initial_hypothesis") or ""
    asset = state.get("asset") or ""

    # Construct clean query for vector embedding
    query_parts = [p for p in [summary, hypothesis, f"asset: {asset}"] if p]
    query = " | ".join(query_parts) if query_parts else "security incident"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.rag_service_url}/rag/search",
                json={"query": query, "top_k": 5},
            )
            response.raise_for_status()
            data = response.json()

        state["threat_intel"] = {
            "status": "ok",
            "query": query,
            "matched_techniques": data.get("hits", []),
        }
    except Exception as exc:
        logger.warning("RAG service unreachable (%s) -- falling back to stub", exc)
        state["threat_intel"] = {
            "status": "stub",
            "note": "RAG service unreachable -- see rag-service/README.md",
            "would_have_searched_for": query,
            "matched_techniques": [],
        }

    state.setdefault("trace", []).append("threat_intel_agent")
    return state