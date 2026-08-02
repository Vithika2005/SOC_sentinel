"""
Consumes from the Normalizer's output topic, runs each event through
IncidentService, and republishes the resulting incident onto the
`incidents` topic -- which your LangGraph pipeline (Recon Agent) consumes.

Kafka(normalized-events) -> Incident Service -> Kafka(incidents) -> LangGraph
"""

import asyncio
import json
import logging
from datetime import datetime

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.config import settings
from app.db.database import db
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentOut, NormalizedEvent
from app.services.incident_service import IncidentService

logger = logging.getLogger("incident-service.kafka")


class IncidentKafkaConsumer:
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
            "Incident service consuming '%s' -> publishing '%s'",
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

    async def _consume_loop(self):
        assert self.consumer is not None

        while True:
            records = await self.consumer.getmany(timeout_ms=5000)

            print("=" * 60)
            print("POLL RESULT:", records)
            print("=" * 60)

            for tp, messages in records.items():
                for msg in messages:
                    print("MESSAGE RECEIVED:", msg.value)

                    try:
                        await self._handle_message(msg.value)
                    except Exception:
                        logger.exception(
                            "Failed to process event: %s",
                            msg.value,
                        )

    async def _handle_message(self, raw: dict):
        print("INSIDE HANDLE MESSAGE")
        print(raw)

        data = raw.get("data", {})

        ts = raw.get("timestamp")

        if isinstance(ts, (int, float)):
            event_time = datetime.utcfromtimestamp(ts)
        else:
            event_time = datetime.utcnow()

        event = NormalizedEvent(
            source_type=data.get("scanner", "unknown"),
            asset=data.get("file", "unknown"),
            message=data.get("description", "No description"),
            severity=data.get("severity", "LOW").lower(),
            timestamp=event_time,
            raw=raw,
        )

        async with db.session_factory() as session:
            repository = IncidentRepository(session)
            service = IncidentService(repository)

            print("CALLING PROCESS_EVENT")

            incident, is_new = await service.process_event(event)

            print("PROCESS_EVENT FINISHED")

            payload = IncidentOut.model_validate(
                incident
            ).model_dump(mode="json")

            payload["is_new"] = is_new

            await self.producer.send_and_wait(
                settings.kafka_output_topic,
                payload,
            )

            logger.info(
                "%s incident %s (asset=%s severity=%s events=%d)",
                "Created" if is_new else "Updated",
                incident.incident_ref,
                incident.asset,
                incident.severity.value,
                incident.event_count,
            )


kafka_consumer = IncidentKafkaConsumer()