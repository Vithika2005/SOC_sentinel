#dashboard-service/app/consumer.py
import json
import logging
import asyncio
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
from config import settings
from database import SessionLocal
from models import IncidentRecord
from websocket import ws_manager
logger = logging.getLogger("dashboard.consumer")

async def consume_agent_recommendations():
    consumer = AIOKafkaConsumer(
        settings.kafka_output_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        auto_offset_reset="earliest"
    )
    await consumer.start()
    logger.info("Kafka consumer started listening on topic: %s", settings.kafka_output_topic)
    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode("utf-8"))
                logger.info("Consumed recommendation for incident: %s", data.get("incident_ref"))
                
                # Persist to Postgres
                db: Session = SessionLocal()
                incident = db.query(IncidentRecord).filter_by(incident_ref=data.get("incident_ref")).first()
                if not incident:
                    incident = IncidentRecord(
                        incident_ref=data.get("incident_ref"),
                        asset=data.get("asset", "unknown"),
                        source_type=data.get("source_type", "unknown"),
                        severity=data.get("severity", "medium"),
                        summary=data.get("summary", ""),
                    )
                    db.add(incident)
                
                incident.recon_findings = data.get("recon_findings")
                incident.threat_intel = data.get("threat_intel")
                incident.risk_assessment = data.get("risk_assessment")
                incident.decision = data.get("decision")
                incident.audit = data.get("audit")
                incident.trace = data.get("trace")
                
                db.commit()
                db.close()

                # Broadcast update to connected frontend consoles via WebSocket
                await ws_manager.broadcast({
                    "event": "INCIDENT_UPDATED",
                    "data": data
                })
            except Exception as e:
                logger.error("Error processing Kafka message: %s", e)
    finally:
        await consumer.stop()