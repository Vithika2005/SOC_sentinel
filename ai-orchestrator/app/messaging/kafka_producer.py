import json

from kafka import KafkaProducer

from app.config.config import settings


class AgentRecommendationProducer:
    """
    Kafka producer responsible for publishing
    agent recommendations to the output topic.
    """

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda value: json.dumps(value).encode("utf-8")
        )

    def publish(self, recommendation: dict):
        """
        Publish the final LangGraph output to Kafka.
        """

        self.producer.send(
            settings.KAFKA_PRODUCER_TOPIC,
            recommendation
        )

        self.producer.flush()

        print("=" * 70)
        print("RECOMMENDATION PUBLISHED")
        print(f"Topic : {settings.KAFKA_PRODUCER_TOPIC}")
        print("=" * 70)