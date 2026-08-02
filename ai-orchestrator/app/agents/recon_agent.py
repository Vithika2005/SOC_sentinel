from app.agents.base_agent import BaseAgent
from app.graph.state import AgentState


class ReconAgent(BaseAgent):
    """
    Stub implementation of the Recon Agent.
    """

    def run(self, state: AgentState) -> AgentState:
        state["recon"] = {
            "status": "completed",
            "summary": "Reconnaissance completed successfully.",
            "identified_asset": state["incident"].get("asset", "Unknown"),
            "possible_attack": "Credential Stuffing",
            "confidence": 0.85
        }

        return state