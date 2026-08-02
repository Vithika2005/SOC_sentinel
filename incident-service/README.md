# SentinelX — Incident Service (Step 11)

Sits between Kafka and the LangGraph agent pipeline:

```
Kafka(normalized-events) → Incident Service → Kafka(incidents) → LangGraph
                                  │
                                  ▼
                              PostgreSQL
```

## What it does

1. **Deduplicate** — a Bloom filter gives a fast in-memory pre-check on every
   event's hash; a Postgres unique constraint on `raw_events.event_hash` is
   the authoritative fallback (Bloom filters can false-positive, never
   false-negative, so this is safe).
2. **Correlate** — events on the same `asset` within a rolling time window
   (`CORRELATION_WINDOW_MINUTES`, default 15) get merged into the same open
   incident instead of spawning duplicates.
3. **Assign Incident ID** — human-readable refs like `INC-20260801-4F2A1B`.
4. **Persist** — incidents + raw events land in Postgres.
5. **Forward** — every create/update republishes the incident as JSON onto
   the `incidents` Kafka topic, which is where your first LangGraph node
   (Recon Agent) should consume from.

## Structure (Controller → Service → Repository → DB, per your notes)

```
app/
├── main.py                    # FastAPI app + lifespan (starts Kafka consumer)
├── config.py                  # env-driven settings
├── db/
│   ├── database.py            # singleton async engine/session
│   └── models.py              # Incident, RawEvent (SQLAlchemy)
├── schemas/incident.py        # Pydantic request/response models
├── core/bloom_filter.py       # dedup pre-check
├── repositories/incident_repository.py
├── services/
│   ├── incident_service.py    # dedup + correlation business logic
│   └── kafka_consumer.py      # consume → process → produce
└── routers/incident_router.py # REST endpoints
```

## REST endpoints

- `GET /incidents` — list, filter by `?status=open`
- `GET /incidents/{id}` — single incident
- `POST /incidents/{id}/resolve` — mark resolved
- `GET /incidents/dashboard/stats` — counts for the dashboard
- `GET /health`

## Running it

Drop this folder in as `sentinelx/incident-service/` next to your existing
`docker-compose.yml`, then merge in `docker-compose.snippet.yml`.

```bash
cp .env.example .env
# edit .env: point KAFKA_INPUT_TOPIC at whatever your Normalizer actually
# publishes to, and KAFKA_BOOTSTRAP_SERVERS at your existing broker

docker compose up -d --build incident-service
```

## Testing without your real Normalizer running yet

```bash
pip install aiokafka
python scripts/send_test_event.py
```

Then check:

```bash
curl http://localhost:8001/incidents
curl http://localhost:8001/incidents/dashboard/stats
```

You should see two incidents: one for `auth-service` (the two failed-login
events correlated together, severity escalated to `high`), and one
`critical` one for `api-service` (SQL injection).

## Next step

Point your first LangGraph node's Kafka consumer at the `incidents` topic —
that's Step 12 (Recon Agent) in your pipeline. Happy to build that next.
