from app.graph.builder import graph

initial_state = {
    "incident": {
        "incident_id": "INC-001",
        "asset": "auth-service",
        "severity": "HIGH",
        "summary": "Multiple failed login attempts"
    },
    "recon": {},
    "threat_intel": {},
    "risk": {},
    "decision": {},
    "audit": {}
}

result = graph.invoke(initial_state)

print("\n===== FINAL PIPELINE OUTPUT =====\n")
print(result)