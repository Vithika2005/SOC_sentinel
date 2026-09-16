# ai-orchestrator/app/services/kafka_bridge.py
"""
    Kafka(incidents) -> LangGraph pipeline -> Kafka(agent-recommendations)

Mirrors the same consume/produce shape as the Incident Service, so the two
services compose cleanly in the same docker-compose network.
"""
import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.config import settings
from app.graph.pipeline import pipeline

logger = logging.getLogger("orchestrator.kafka")


class OrchestratorKafkaBridge:
    def __init__(self):
        self.consumer: AIOKafkaConsumer | None = None
        self.producer: AIOKafkaProducer | None = None
        self._task: asyncio.Task | None = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            settings.kafka_input_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_consumer_group,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        )
        await self.consumer.start()
        await self.producer.start()
        self._task = asyncio.create_task(self._consume_loop())
        logger.info(
            "AI Orchestrator consuming '%s' -> publishing '%s'",
            settings.kafka_input_topic,
            settings.kafka_output_topic,
        )

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()

    async def send(self, topic: str, value: dict):
        """Publish a message directly to a Kafka topic."""
        if not self.producer:
            raise RuntimeError("Kafka producer is not initialized or started.")
        await self.producer.send_and_wait(topic, value)

    async def _consume_loop(self):
        assert self.consumer is not None
        async for msg in self.consumer:
            try:
                await self._handle_incident(msg.value)
            except Exception:
                logger.exception("Pipeline failed for incident: %s", msg.value)

    async def _handle_incident(self, incident: dict):
        # incident is the JSON payload produced by the Incident Service
        initial_state = {
            "incident_id": incident.get("id"),
            "incident_ref": incident.get("incident_ref"),
            "asset": incident.get("asset"),
            "source_type": incident.get("source_type"),
            "severity": incident.get("severity"),
            "summary": incident.get("summary"),
            "event_count": incident.get("event_count", 1),
            "trace": [],
        }

        result = await pipeline.ainvoke(initial_state)

        await self.send(settings.kafka_output_topic, result)
        logger.info(
            "Pipeline complete for %s -> recommendation: %s",
            result.get("incident_ref"),
            (result.get("decision") or {}).get("recommendation"),
        )


kafka_bridge = OrchestratorKafkaBridge()