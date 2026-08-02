from app.agents.base_agent import BaseAgent
from app.graph.state import AgentState


class DecisionAgent(BaseAgent):
    """
    Stub implementation of the Decision Agent.
    """

    def run(self, state: AgentState) -> AgentState:
        state["decision"] = {
            "status": "completed",
            "recommendation": "Escalate incident to SOC analyst",
            "priority": "High",
            "action": "Open investigation ticket"
        }

        return state