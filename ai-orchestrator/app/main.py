from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI

from app.api.pipeline import router
from app.config.config import settings
from app.messaging.kafka_consumer import IncidentConsumer


consumer = IncidentConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start background services when FastAPI starts.
    """

    consumer_thread = threading.Thread(
        target=consumer.start,
        daemon=True
    )

    consumer_thread.start()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "SentinelX AI Orchestrator is running."
    }