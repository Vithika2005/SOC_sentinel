from app.agents.base_agent import BaseAgent
from app.graph.state import AgentState


class RiskAgent(BaseAgent):
    """
    Stub implementation of the Risk Assessment Agent.
    """

    def run(self, state: AgentState) -> AgentState:
        state["risk"] = {
            "status": "completed",
            "risk_score": 75,
            "risk_level": "High",
            "business_impact": "Potential unauthorized access",
            "remarks": "Static risk assessment."
        }

        return state