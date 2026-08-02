from typing import TypedDict, Dict, Any


class AgentState(TypedDict):
    """
    Shared state that flows through the LangGraph pipeline.
    """

    incident: Dict[str, Any]
    recon: Dict[str, Any]
    threat_intel: Dict[str, Any]
    risk: Dict[str, Any]
    decision: Dict[str, Any]
    audit: Dict[str, Any]


def create_initial_state(incident: Dict[str, Any]) -> AgentState:
    """
    Create the initial state for the LangGraph pipeline.
    """

    return {
        "incident": incident,
        "recon": {},
        "threat_intel": {},
        "risk": {},
        "decision": {},
        "audit": {},
    }