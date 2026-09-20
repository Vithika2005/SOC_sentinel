from pathlib import Path
import os

DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent

FINDINGS_FILE = PROJECT_ROOT / "sentinelx_findings.json"

AI_ORCHESTRATOR_URL = os.getenv(
    "AI_ORCHESTRATOR_URL",
    "http://localhost:8002"
)

INCIDENT_SERVICE_URL = os.getenv(
    "INCIDENT_SERVICE_URL",
    "http://localhost:8001"
)

DIGITAL_TWIN_URL = os.getenv(
    "DIGITAL_TWIN_URL",
    "http://localhost:8003"
)

RAG_SERVICE_URL = os.getenv(
    "RAG_SERVICE_URL",
    "http://localhost:8004"
)

NEO4J_URI = os.getenv(
    "NEO4J_URI",
    "bolt://localhost:7687"
)

NEO4J_USER = os.getenv(
    "NEO4J_USER",
    "neo4j"
)

NEO4J_PASSWORD = os.getenv(
    "NEO4J_PASSWORD",
    "password123"
)

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://localhost:9090",
)

GRAFANA_URL = os.getenv(
    "GRAFANA_URL",
    "http://localhost:3000/d/sentinelx-monitoring/sentinelx-monitoring",
)