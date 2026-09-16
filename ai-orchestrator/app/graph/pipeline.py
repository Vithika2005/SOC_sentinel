import os
from fastapi import APIRouter, HTTPException
from langgraph.graph import END, StateGraph
from typing import Dict, Any

from app.graph.factory import AgentFactory
from app.graph.state import AgentState

KAFKA_OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "agent-recommendations")

router = APIRouter(
    prefix="/pipeline",
    tags=["Pipeline"]
)

@router.post("/run")
async def run_pipeline(initial_state: Dict[str, Any]):
    """
    Executes the LangGraph incident analysis pipeline and publishes to Kafka.
    """
    # Import locally to avoid circular import issues on startup
    from app.services.kafka_bridge import kafka_bridge

    try:
        final_state = await pipeline.ainvoke(initial_state)
        await kafka_bridge.send(KAFKA_OUTPUT_TOPIC, final_state)
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


PIPELINE_ORDER = ["recon", "threat_intel", "risk", "decision", "auditor"]

def _node_id(agent_type: str) -> str:
    return f"{agent_type}_agent"

def build_pipeline():
    graph = StateGraph(AgentState)

    for name in PIPELINE_ORDER:
        graph.add_node(_node_id(name), AgentFactory.get(name))

    graph.set_entry_point(_node_id(PIPELINE_ORDER[0]))
    for current, nxt in zip(PIPELINE_ORDER, PIPELINE_ORDER[1:]):
        graph.add_edge(_node_id(current), _node_id(nxt))
    graph.add_edge(_node_id(PIPELINE_ORDER[-1]), END)

    return graph.compile()

pipeline = build_pipeline()