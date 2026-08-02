import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "sentinelx-security-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="sentinelx-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening...")

for message in consumer:

    event = message.value

    finding = event["data"]

    print("=" * 60)

    print("Finding ID :", finding.get("id"))

    print("Severity   :", finding.get("severity"))

    print("Tool       :", finding.get("tool"))

    print("Title      :", finding.get("title"))