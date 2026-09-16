"""STEP 12b -- Decision Agent (real). Synthesizes everything gathered so far
into a concrete recommendation. Already usable today even though threat_intel
and risk_assessment are still stubs -- it just has less to work with until
Steps 13/14 are wired in."""
import json
import logging

from app.core.llm_client import llm_client
from app.graph.state import AgentState

logger = logging.getLogger("orchestrator.decision")

SYSTEM_PROMPT = """You are the Decision Agent in SentinelX. Synthesize the recon findings,
threat intel, and risk assessment into a remediation recommendation. Respond ONLY with JSON:
{
  "recommendation": "<concrete remediation action>",
  "confidence": "<low|medium|high>",
  "reasoning": "<short justification tying together the inputs>",
  "requires_human_review": true/false
}
If threat_intel or risk_assessment are marked as stubs with no real data, say so in the
reasoning and lower your confidence accordingly."""


async def decision_agent(state: AgentState) -> AgentState:
    user_prompt = json.dumps(
        {
            "incident_ref": state.get("incident_ref"),
            "asset": state.get("asset"),
            "severity": state.get("severity"),
            "recon_findings": state.get("recon_findings"),
            "threat_intel": state.get("threat_intel"),
            "risk_assessment": state.get("risk_assessment"),
        },
        default=str,
    )

    raw = llm_client.complete_json(SYSTEM_PROMPT, user_prompt)
    try:
        decision = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Decision agent returned non-JSON, wrapping raw text")
        decision = {"raw_response": raw, "requires_human_review": True}

    state["decision"] = decision
    state.setdefault("trace", []).append("decision_agent")
    return state
