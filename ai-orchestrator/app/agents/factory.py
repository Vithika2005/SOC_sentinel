from app.agents.recon_agent import ReconAgent
from app.agents.threat_intel_agent import ThreatIntelAgent
from app.agents.risk_agent import RiskAgent
from app.agents.decision_agent import DecisionAgent
from app.agents.auditor_agent import AuditorAgent


class AgentFactory:
    """
    Factory class responsible for creating agent instances.
    """

    @staticmethod
    def get_agent(agent_name: str):
        agents = {
            "recon": ReconAgent(),
            "threat_intel": ThreatIntelAgent(),
            "risk": RiskAgent(),
            "decision": DecisionAgent(),
            "auditor": AuditorAgent(),
        }

        if agent_name not in agents:
            raise ValueError(f"Unknown agent: {agent_name}")

        return agents[agent_name]