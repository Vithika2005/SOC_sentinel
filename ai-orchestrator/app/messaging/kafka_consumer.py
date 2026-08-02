import json

from kafka import KafkaConsumer

from app.config.config import settings
from app.messaging.kafka_producer import AgentRecommendationProducer
from app.services.pipeline_service import PipelineService


class IncidentConsumer:
    """
    Kafka consumer responsible for receiving incidents,
    executing the LangGraph pipeline, and publishing
    the recommendations.
    """

    def __init__(self):

        self.consumer = KafkaConsumer(
            settings.KAFKA_CONSUMER_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="sentinelx-ai-orchestrator",
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

        self.producer = AgentRecommendationProducer()

    def start(self):
        """
        Start consuming incidents from Kafka.
        """

        print("Waiting for incidents...")

        for message in self.consumer:

            incident = message.value

            print(f"\nReceived Incident:\n{incident}")

            result = PipelineService.execute(incident)

            print("\nPipeline Execution Completed")

            self.producer.publish(result)

            print("Recommendation published successfully.")