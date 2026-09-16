"""STEP 12a -- Recon Agent (real). First node in the pipeline: takes the raw
incident and produces an initial triage before any RAG or graph lookups."""
import json
import logging

from app.core.llm_client import llm_client
from app.graph.state import AgentState

logger = logging.getLogger("orchestrator.recon")

SYSTEM_PROMPT = """You are the Recon Agent in SentinelX, an AI security operations platform.
Given a raw incident, produce an initial triage. Respond ONLY with JSON, no prose, no markdown fences:
{
  "attack_surface": "<short description of what part of the system is affected>",
  "initial_hypothesis": "<best guess of what's happening>",
  "indicators_to_check": ["<indicator 1>", "<indicator 2>"],
  "recommended_next_agent_focus": "<what the Threat Intel Agent should search for>"
}"""


async def recon_agent(state: AgentState) -> AgentState:
    user_prompt = (
        f"Incident: {state.get('incident_ref')}\n"
        f"Asset: {state.get('asset')}\n"
        f"Source type: {state.get('source_type')}\n"
        f"Severity: {state.get('severity')}\n"
        f"Event count: {state.get('event_count')}\n"
        f"Summary: {state.get('summary') or 'n/a'}"
    )

    raw = llm_client.complete_json(SYSTEM_PROMPT, user_prompt)
    try:
        findings = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Recon agent returned non-JSON, wrapping raw text")
        findings = {"raw_response": raw}

    state["recon_findings"] = findings
    state.setdefault("trace", []).append("recon_agent")
    return state
