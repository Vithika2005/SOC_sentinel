from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState
from app.agents.factory import AgentFactory


# Create agent instances
recon_agent = AgentFactory.get_agent("recon")
threat_intel_agent = AgentFactory.get_agent("threat_intel")
risk_agent = AgentFactory.get_agent("risk")
decision_agent = AgentFactory.get_agent("decision")
auditor_agent = AgentFactory.get_agent("auditor")


# Wrapper functions for LangGraph
def recon_node(state: AgentState):
    return recon_agent.run(state)


def threat_intel_node(state: AgentState):
    return threat_intel_agent.run(state)


def risk_node(state: AgentState):
    return risk_agent.run(state)


def decision_node(state: AgentState):
    return decision_agent.run(state)


def auditor_node(state: AgentState):
    return auditor_agent.run(state)


# Build the graph
builder = StateGraph(AgentState)

builder.add_node("recon_node", recon_node)
builder.add_node("threat_intel_node", threat_intel_node)
builder.add_node("risk_node", risk_node)
builder.add_node("decision_node", decision_node)
builder.add_node("auditor_node", auditor_node)

builder.add_edge(START, "recon_node")
builder.add_edge("recon_node", "threat_intel_node")
builder.add_edge("threat_intel_node", "risk_node")
builder.add_edge("risk_node", "decision_node")
builder.add_edge("decision_node", "auditor_node")
builder.add_edge("auditor_node", END)

graph = builder.compile()