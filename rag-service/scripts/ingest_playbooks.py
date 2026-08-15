"""
Ingests internal remediation playbooks (markdown files) into Qdrant.
Drop your own .md files into the playbooks/ directory -- one file per
playbook, first line (a "# Heading") is treated as the title.

Usage:
    cd rag-service
    python scripts/ingest_playbooks.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.services.ingest_service import ingest_documents  # noqa: E402

PLAYBOOKS_DIR = Path(__file__).parent.parent / "playbooks"


def load_playbooks() -> list[dict]:
    documents = []
    for path in sorted(PLAYBOOKS_DIR.glob("*.md")):
        text = path.read_text()
        title = text.splitlines()[0].lstrip("#").strip() if text.strip() else path.stem
        documents.append(
            {
                "source": "playbook",
                "title": title,
                "text": text,
                "metadata": {"filename": path.name},
            }
        )
    return documents


def main():
    documents = load_playbooks()
    if not documents:
        print(f"No playbooks found in {PLAYBOOKS_DIR}. Add .md files there first.")
        return
    count = ingest_documents(documents)
    print(f"Ingested {count} playbooks into Qdrant")


if __name__ == "__main__":
    main()
