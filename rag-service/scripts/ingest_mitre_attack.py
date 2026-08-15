"""
Downloads the MITRE ATT&CK Enterprise matrix (STIX 2.1 bundle, official
mitre-attack/attack-stix-data repo on GitHub) and ingests each technique's
name + description into Qdrant.

Usage:
    cd rag-service
    python scripts/ingest_mitre_attack.py
"""
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.services.ingest_service import ingest_documents  # noqa: E402

import re

MITRE_URL = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/"
    "master/enterprise-attack/enterprise-attack.json"
)

CITATION_PATTERN = re.compile(r"\(Citation:[^)]*\)")


def fetch_techniques() -> list[dict]:
    print(f"Downloading MITRE ATT&CK STIX bundle from {MITRE_URL} ...")
    resp = httpx.get(MITRE_URL, timeout=180.0)
    resp.raise_for_status()
    bundle = resp.json()

    documents = []
    for obj in bundle.get("objects", []):
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        technique_id = next(
            (
                ref["external_id"]
                for ref in obj.get("external_references", [])
                if ref.get("source_name") == "mitre-attack"
            ),
            None,
        )
        if not technique_id:
            continue

        tactics = [phase["phase_name"] for phase in obj.get("kill_chain_phases", [])]
        # first paragraph is usually a self-contained summary; STIX descriptions
        # can run long and include markdown tables we don't need for embedding
        description = obj.get("description", "").split("\n")[0].strip()
        description = CITATION_PATTERN.sub("", description).strip()
        name = obj.get("name", "")

        documents.append(
            {
                "source": "mitre",
                "title": f"{technique_id}: {name}",
                "text": f"{name} ({technique_id}). {description}",
                "metadata": {"technique_id": technique_id, "tactics": tactics},
            }
        )

    return documents


def main():
    documents = fetch_techniques()
    print(f"Parsed {len(documents)} MITRE ATT&CK techniques")
    count = ingest_documents(documents)
    print(f"Ingested {count} documents into Qdrant collection")


if __name__ == "__main__":
    main()
