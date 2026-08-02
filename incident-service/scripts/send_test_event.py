"""
Fire a handful of test events straight onto the input topic, bypassing your
real Normalizer, so you can confirm the Incident Service is wired up before
plugging it into the live pipeline.

Usage:
    pip install aiokafka
    python scripts/send_test_event.py
"""
import asyncio
import json
import os
import time

from aiokafka import AIOKafkaProducer

BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.environ.get("KAFKA_INPUT_TOPIC", "normalized-events")

EVENTS = [
    {"source_type": "runtime", "asset": "auth-service", "severity": "medium", "message": "Repeated failed login attempts", "raw": {"ip": "203.0.113.5", "attempts": 8}},
    {"source_type": "runtime", "asset": "auth-service", "severity": "high", "message": "Failed login threshold exceeded", "raw": {"ip": "203.0.113.5", "attempts": 20}},
    {"source_type": "appsec", "asset": "api-service", "severity": "critical", "message": "SQL injection pattern detected", "raw": {"rule": "sqli-001", "endpoint": "/users"}},
]


async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await producer.start()
    try:
        for event in EVENTS:
            event["timestamp"] = time.time()
            await producer.send_and_wait(TOPIC, event)
            print(f"sent: {event['asset']} / {event['message']}")
            await asyncio.sleep(1)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
