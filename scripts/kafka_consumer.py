import json
from kafka import KafkaConsumer

KAFKA_TOPIC = "sentinelx-security-events"
KAFKA_SERVER = "localhost:9092"


def run_consumer():

    print(f"Connecting to {KAFKA_SERVER}")

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="sentinelx-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print("Waiting for events...\n")

    for message in consumer:

        event = message.value

        finding = event["data"]

        print("=" * 70)
        print("EVENT RECEIVED")
        print("=" * 70)

        print("Scanner    :", finding.get("scanner"))
        print("Type       :", finding.get("type"))
        print("Severity   :", finding.get("severity"))
        print("Rule ID    :", finding.get("rule_id"))
        print("Description:", finding.get("description"))
        print("Location   :", finding.get("location", finding.get("file")))
        print()


if __name__ == "__main__":
    run_consumer()