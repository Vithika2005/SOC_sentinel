# SentinelX — RAG Service (Step 13)

Populates Qdrant with security knowledge and exposes it for search:

```
MITRE ATT&CK ─┐
OWASP Top 10 ─┼─► embed (all-MiniLM-L6-v2) ─► Qdrant ─► /rag/search ─► Threat Intel Agent
Playbooks    ─┘
```

## Structure

```
app/
├── main.py                    # FastAPI app
├── config.py
├── core/
│   ├── embeddings.py          # singleton SentenceTransformer
│   └── vector_store.py        # singleton Qdrant client, auto-creates collection
├── schemas.py
├── services/
│   ├── ingest_service.py      # embed + upsert documents
│   └── search_service.py      # embed query + search, optional source filter
└── routers/rag_router.py      # POST /rag/search, POST /rag/ingest, GET /rag/stats

scripts/
├── ingest_mitre_attack.py     # live-fetches MITRE's STIX bundle from GitHub, ~700 techniques
├── ingest_owasp_top10.py      # curated OWASP Top 10 2021 categories
└── ingest_playbooks.py        # loads playbooks/*.md

playbooks/
├── brute_force_response.md    # example internal playbook
└── sql_injection_response.md  # example internal playbook
```

Verified against real data while building this: the MITRE fetch actually
pulls and parses ~700 live techniques from
`mitre-attack/attack-stix-data` on GitHub (confirmed `T1110` Brute Force
parses correctly, citation footnotes stripped from descriptions). Ingest →
search → source-filter was tested end-to-end against a real Qdrant instance.

## REST endpoints

- `POST /rag/search` — `{"query": "...", "top_k": 5, "source_filter": "mitre"}` (`source_filter` optional: `mitre` | `owasp` | `playbook`)
- `POST /rag/ingest` — ad-hoc one-off document ingestion
- `GET /rag/stats` — point count in the collection
- `GET /health`

## Running it

Drop this folder in as `sentinelx/rag-service/`, merge in
`docker-compose.snippet.yml` (adds both `qdrant` and `rag-service`, plus a
named volume for Qdrant's data).

```bash
cp .env.example .env
docker compose up -d --build qdrant rag-service
```

## Loading the knowledge base

Run once after the service is up (needs internet access for the MITRE
download and the first embedding-model load):

```bash
pip install -r requirements.txt   # if running locally rather than in the container
python scripts/ingest_mitre_attack.py    # ~700 techniques, takes a minute
python scripts/ingest_owasp_top10.py     # instant
python scripts/ingest_playbooks.py       # loads playbooks/*.md — add your own here
```

Or exec into the running container and run them there, so they use the
container's already-downloaded model and can reach `qdrant` by hostname:

```bash
docker compose exec rag-service python scripts/ingest_mitre_attack.py
docker compose exec rag-service python scripts/ingest_owasp_top10.py
docker compose exec rag-service python scripts/ingest_playbooks.py
```

## Testing

```bash
curl -X POST http://localhost:8003/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "repeated failed login attempts", "top_k": 3}'
```

Should surface `T1110: Brute Force` from MITRE, `A07:2021: Identification
and Authentication Failures` from OWASP, and the `Brute Force / Credential
Stuffing Response` playbook.

```bash
curl http://localhost:8003/rag/stats
```

## Wiring into the AI Orchestrator

Already done — `ai-orchestrator`'s `threat_intel_agent` now calls this
service's `/rag/search` with whatever Recon flagged as worth investigating,
and gracefully falls back to a stub response if this service isn't reachable
(so you can deploy it after the orchestrator without breaking anything).

## Next step

Step 14: stand up Neo4j as the Digital Twin and replace the Risk Agent stub
with real blast-radius queries. Want that next?
