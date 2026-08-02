import json
import logging

from kafka import KafkaConsumer

from app.config.config import settings
from app.messaging.kafka_producer import AgentRecommendationProducer
from app.services.pipeline_service import PipelineService

logger = logging.getLogger("ai-orchestrator.kafka")


class OrchestratorKafkaConsumer:
    """
    Consumes incidents published by the Incident Service,
    executes the LangGraph pipeline and publishes the
    recommendations to the output Kafka topic.
    """

    def __init__(self):

        self.consumer = KafkaConsumer(
            settings.KAFKA_CONSUMER_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="sentinelx-ai-orchestrator",
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        )

        self.pipeline_service = PipelineService()
        self.producer = AgentRecommendationProducer()

    def start(self):
        """
        Start consuming incidents.
        """

        logger.info(
            "Listening on topic '%s'",
            settings.KAFKA_CONSUMER_TOPIC,
        )

        for message in self.consumer:

            print("=" * 70)
            print("INCIDENT RECEIVED FROM KAFKA")
            print(message.value)
            print("=" * 70)

            try:
                self._handle_message(message.value)

            except Exception:
                logger.exception("Failed to process incident")

    def _handle_message(self, incident: dict):
        """
        Process one incident received from Kafka.
        """
        print("RUNNING LANGGRAPH PIPELINE...")

        logger.info(
            "Processing incident %s",
            incident.get("incident_ref"),
        )

        result = self.pipeline_service.execute(incident)

        self.producer.publish(result)

        logger.info(
            "Recommendation published for %s",
            incident.get("incident_ref"),
        )