from app.agents.base_agent import BaseAgent
from app.graph.state import AgentState


class ThreatIntelAgent(BaseAgent):
    """
    Stub implementation of the Threat Intelligence Agent.
    """

    def run(self, state: AgentState) -> AgentState:
        state["threat_intel"] = {
            "status": "completed",
            "known_threat": False,
            "ioc_match": False,
            "threat_level": "Low",
            "remarks": "Static threat intelligence response."
        }

        return state