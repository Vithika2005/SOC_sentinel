# SentinelX — Digital Twin (Step 14)

Neo4j graph of your **enterprise** assets (the app being protected — not
SentinelX's own microservices), used to answer "what if this asset is
isolated?" with a real graph algorithm instead of a lookup table.

```
Internet → nginx → api-service → postgres
                 → auth-service ↗
```

## The algorithm (verified against your exact notes example)

For asset `X` with entrypoint `Internet` (configurable):

1. **`direct_dependents`** — assets with an edge pointing at `X` (who calls it)
2. **`direct_dependencies`** — assets `X` points at (what it calls)
3. **`services_unreachable_if_isolated`** — remove `X` from the graph, see
   which assets that were reachable from `Internet` no longer are. This is
   what catches "Database is only reachable through API" — a flat
   dependency list would miss that it's a single point of failure.
4. **`affected_services`** = union of (1) and (3)

Tested against your notes' exact example — `Internet → Nginx → API →
Database`, isolate `API`:

```json
{
  "direct_dependents": ["Nginx"],
  "direct_dependencies": ["Database"],
  "services_unreachable_if_isolated": ["Database"],
  "affected_services": ["Database", "Nginx"],
  "affected_count": 2
}
```

Matches "Database unavailable, 2 services affected" exactly. Also verified
against a branching topology (two paths to the same downstream asset) to
confirm it correctly recognizes redundant paths and does *not* over-report
things as unreachable when an alternate route exists.

## Structure

```
app/
├── main.py
├── config.py
├── core/neo4j_client.py       # singleton Neo4j driver
├── schemas.py
├── services/twin_service.py   # seed_topology, get_graph, compute_blast_radius
└── routers/twin_router.py     # POST /twin/seed, GET /twin/blast-radius/{asset}, GET /twin/graph

scripts/
└── seed_topology.py           # your enterprise topology -- edit this as your architecture grows
```

## REST endpoints

- `POST /twin/seed` — `{"edges": [{"source": "nginx", "target": "api-service"}]}`
- `GET /twin/blast-radius/{asset}?entrypoint=Internet` — the blast radius computation
- `GET /twin/graph` — node/edge counts and node list
- `GET /health`

## Running it

Drop this in as `sentinelx/digital-twin/`, merge `docker-compose.snippet.yml`
(adds `neo4j` + `digital-twin`, plus a named volume).

```bash
cp .env.example .env
docker compose up -d --build neo4j digital-twin
```

## Seeding your topology

`scripts/seed_topology.py` has a starter topology matching your
`enterprise/` folder (nginx → frontend/api-service/auth-service/file-service/
legacy-admin → postgres/redis). Edit the `ENTERPRISE_TOPOLOGY` list as your
real architecture grows, then:

```bash
docker compose exec digital-twin python scripts/seed_topology.py
```

You can also browse the graph visually at `http://localhost:7474` (Neo4j
Browser) with the credentials from `.env`.

## Testing

```bash
curl http://localhost:8004/twin/blast-radius/auth-service
```

With the starter topology, isolating `auth-service` should show `nginx` and
`api-service` as affected (they call it directly), but `postgres` stays
reachable — `api-service`, `file-service`, and `legacy-admin` all have their
own direct paths to it.

```bash
curl http://localhost:8004/twin/graph
```

## Wiring into the AI Orchestrator

Already done — `ai-orchestrator`'s `risk_agent` now calls this service's
`/twin/blast-radius/{asset}`, using severity + blast radius together. It
falls back to a stub if this service is unreachable, and returns
`unknown_asset` (not an error) if the incident's asset hasn't been seeded
into the twin yet.

## Next step

Step 15: wire up DeepEval/RAGAS and replace the Auditor Agent stub — the
last piece before every agent in the pipeline is real. Want that next?
