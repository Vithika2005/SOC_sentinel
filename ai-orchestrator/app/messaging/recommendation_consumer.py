import json

from kafka import KafkaConsumer

from app.config.config import settings


def run_consumer():
    """
    Test consumer for verifying that the AI Orchestrator
    publishes recommendations correctly.
    """

    consumer = KafkaConsumer(
        settings.KAFKA_PRODUCER_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="recommendation-test-group",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    print("=" * 70)
    print(f"Listening on topic: {settings.KAFKA_PRODUCER_TOPIC}")
    print("=" * 70)

    for message in consumer:

        print("=" * 70)
        print("RECOMMENDATION RECEIVED")
        print(message.value)
        print("=" * 70)


if __name__ == "__main__":
    run_consumer()