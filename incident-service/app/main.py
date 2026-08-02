import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import init_models
from app.routers.incident_router import router as incident_router
from app.services.kafka_consumer import kafka_consumer

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    await kafka_consumer.start()
    yield
    await kafka_consumer.stop()


app = FastAPI(title="SentinelX Incident Service", version="0.1.0", lifespan=lifespan)
app.include_router(incident_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
