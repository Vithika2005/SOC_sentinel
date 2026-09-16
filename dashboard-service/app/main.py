import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import IncidentRecord
from consumer import consume_agent_recommendations
from websocket import ws_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dashboard.main")

# Auto-create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Startup: Launch background Kafka consumer
    consumer_task = asyncio.create_task(consume_agent_recommendations())
    logger.info("Background Kafka consumer started.")
    yield
    # Shutdown: Clean up task
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        logger.info("Kafka consumer task stopped.")

# THIS VARIABLE NAME MUST BE EXACTLY 'app'
app = FastAPI(
    title="SentinelX Dashboard Service",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "dashboard-service"}

@app.get("/api/v1/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(IncidentRecord).order_by(IncidentRecord.created_at.desc()).all()

@app.get("/api/v1/incidents/{incident_ref}")
def get_incident(incident_ref: str, db: Session = Depends(get_db)):
    incident = db.query(IncidentRecord).filter(IncidentRecord.incident_ref == incident_ref).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)