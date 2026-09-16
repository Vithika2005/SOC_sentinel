"""
Seeds the Digital Twin with your enterprise topology (the application
SentinelX protects -- auth-service, api-service, etc from your
`enterprise/` folder. NOT SentinelX's own microservices).

Edit ENTERPRISE_TOPOLOGY below to match your real architecture as it grows.
Each tuple is (source, source_type, target, target_type) meaning
"source calls/depends on target".

Usage:
    cd digital-twin
    python scripts/seed_topology.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.services.twin_service import seed_topology  # noqa: E402

ENTERPRISE_TOPOLOGY = [
    ("Internet", "external", "nginx", "gateway"),
    ("nginx", "gateway", "frontend", "service"),
    ("nginx", "gateway", "api-service", "service"),
    ("nginx", "gateway", "auth-service", "service"),
    ("nginx", "gateway", "file-service", "service"),
    ("nginx", "gateway", "legacy-admin", "service"),

    # api-service depends on auth-service to validate tokens, and reaches
    # postgres directly too -- so auth-service isn't a single point of
    # failure for postgres reachability, just for token validation itself.
    ("api-service", "service", "auth-service", "service"),
    ("api-service", "service", "postgres", "database"),
    ("api-service", "service", "redis", "cache"),

    ("auth-service", "service", "postgres", "database"),
    ("file-service", "service", "postgres", "database"),
    ("legacy-admin", "service", "postgres", "database"),
]


def main():
    count = seed_topology(ENTERPRISE_TOPOLOGY)
    print(f"Seeded {count} edges into the Digital Twin")


if __name__ == "__main__":
    main()
