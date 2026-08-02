from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI

from app.api.pipeline import router
from app.config.config import settings
from app.messaging.kafka_consumer import OrchestratorKafkaConsumer


consumer = OrchestratorKafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Starts the Kafka consumer in a background thread when the
    AI Orchestrator starts.
    """

    consumer_thread = threading.Thread(
        target=consumer.start,
        daemon=True,
    )

    consumer_thread.start()

    print("=" * 60)
    print("SentinelX AI Orchestrator Started")
    print(f"Listening on Kafka Topic : {settings.KAFKA_CONSUMER_TOPIC}")
    print("=" * 60)

    yield

    print("Shutting down AI Orchestrator...")


app = FastAPI(
    title="SentinelX AI Orchestrator",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "SentinelX AI Orchestrator is running."
    }