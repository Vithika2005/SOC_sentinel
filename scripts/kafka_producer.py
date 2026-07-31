import json
import time
from kafka import KafkaProducer

KAFKA_TOPIC = "sentinelx-security-events"
KAFKA_SERVER = "localhost:9092"
FINDINGS_FILE = "sentinelx_findings.json"


def run_producer():

    print(f"[*] Connecting to Kafka at {KAFKA_SERVER}...")

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    try:
        with open(FINDINGS_FILE, "r") as f:
            findings = json.load(f)

    except FileNotFoundError:
        print("sentinelx_findings.json not found")
        return

    print(f"Publishing {len(findings)} findings...\n")

    for finding in findings:

        event = {
            "event_type": "SECURITY_FINDING_INGESTED",
            "timestamp": time.time(),
            "data": finding
        }

        producer.send(KAFKA_TOPIC, value=event)

        print(
            f"[+] "
            f"{finding.get('scanner')} | "
            f"{finding.get('severity')} | "
            f"{finding.get('description')}"
        )

        time.sleep(0.1)

    producer.flush()

    print("\nAll findings sent successfully.")


if __name__ == "__main__":
    run_producer()