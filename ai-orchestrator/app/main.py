import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.graph.factory import AgentFactory
from app.graph.pipeline import router as pipeline_router
from app.services.kafka_bridge import kafka_bridge

logging.basicConfig(level=logging.INFO)

KAFKA_OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "agent-recommendations")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_bridge.start()
    yield
    await kafka_bridge.stop()


app = FastAPI(
    title="SentinelX AI Orchestrator", 
    version="0.1.0", 
    lifespan=lifespan
)

# Mount the pipeline router
app.include_router(pipeline_router)


class ManualIncident(BaseModel):
    incident_ref: str = "INC-TEST-000001"
    asset: str
    source_type: str = "runtime"
    severity: str = "medium"
    summary: str | None = None
    event_count: int = 1


@app.post("/pipeline/run")
async def run_pipeline_manually(incident: ManualIncident):
    """Run the agent pipeline and publish result to Kafka for DB persistence."""
    state = {**incident.model_dump(), "incident_id": "manual-test", "trace": []}
    result = await pipeline.ainvoke(state)
    
    # Send pipeline findings to Kafka so dashboard-service inserts them into PostgreSQL
    await kafka_bridge.send(KAFKA_OUTPUT_TOPIC, result)
    
    return result


@app.get("/pipeline/agents")
async def list_agents():
    return {"agents": AgentFactory.available()}


@app.get("/health")
async def health():
    return {"status": "ok"}