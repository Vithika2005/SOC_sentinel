import json
import time
import sys
from kafka import KafkaProducer

# Default to pipeline entry topic; allow overriding via CLI arg
KAFKA_TOPIC = sys.argv[1] if len(sys.argv) > 1 else "sentinelx-security-events"
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
        print(f"[!] {FINDINGS_FILE} not found. Run ingest_devsecops.py first.")
        return

    print(f"[*] Publishing {len(findings)} finding(s) to topic: '{KAFKA_TOPIC}'...\n")

    for finding in findings:
        event = {
            "incident_ref": finding.get("id", f"INC-{int(time.time())}"),
            "asset": finding.get("file") or finding.get("package") or "auth-service",
            "source_type": finding.get("type", "runtime"),
            "severity": finding.get("severity", "medium").lower(),
            "summary": finding.get("description") or finding.get("title") or "Security finding ingested",
            "data": finding
        }

        producer.send(KAFKA_TOPIC, value=event)
        print(f"[+] [{finding.get('scanner', 'unknown')}] {event['severity'].upper()} -> {event['summary'][:60]}")
        time.sleep(0.05)

    producer.flush()
    print("\n[✓] All findings successfully published to Kafka.")

if __name__ == "__main__":
    run_producer()