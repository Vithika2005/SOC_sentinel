#ai-orchestrator/app/test_pipeline.py
# ai-orchestrator/app/test_pipeline.py
from app.graph.pipeline import pipeline

initial_state = {
    "incident_id": "INC-001",
    "incident_ref": "INC-TEST-000001",
    "asset": "auth-service",
    "source_type": "runtime",
    "severity": "high",
    "summary": "Multiple failed login attempts",
    "event_count": 1,
    "trace": [],
}

import asyncio
result = asyncio.run(pipeline.ainvoke(initial_state))
print("\n===== FINAL PIPELINE OUTPUT =====\n")
print(result)