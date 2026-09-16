"""
Factory Pattern for agents (your notes: Design Patterns -> Factory Pattern:
for agents -> Recon, Threat, Risk, Decision). Centralizes agent creation so
the graph wiring in pipeline.py doesn't need to know about each agent's
internals, and new agent types register here in one place.
"""
from app.graph.nodes.auditor import auditor_agent
from app.graph.nodes.decision import decision_agent
from app.graph.nodes.recon import recon_agent
from app.graph.nodes.risk import risk_agent
from app.graph.nodes.threat_intel import threat_intel_agent


class AgentFactory:
    _registry = {
        "recon": recon_agent,
        "threat_intel": threat_intel_agent,
        "risk": risk_agent,
        "decision": decision_agent,
        "auditor": auditor_agent,
    }

    @classmethod
    def get(cls, agent_type: str):
        if agent_type not in cls._registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._registry[agent_type]

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._registry.keys())
