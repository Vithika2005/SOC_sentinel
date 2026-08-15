"""
Ingests the OWASP Top 10 (2021 edition) as reference documents.

This is a curated summary rather than a live scrape -- these ten category
names and one-line descriptions are stable, well-known reference material.
Update OWASP_TOP_10 below when the next edition is published.

Usage:
    cd rag-service
    python scripts/ingest_owasp_top10.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.services.ingest_service import ingest_documents  # noqa: E402

OWASP_TOP_10 = [
    {"id": "A01:2021", "name": "Broken Access Control",
     "summary": "Restrictions on what authenticated users are allowed to do are not properly enforced, letting attackers act outside their intended permissions."},
    {"id": "A02:2021", "name": "Cryptographic Failures",
     "summary": "Sensitive data is exposed due to weak, missing, or misconfigured encryption in transit or at rest."},
    {"id": "A03:2021", "name": "Injection",
     "summary": "Untrusted input is passed to an interpreter as part of a command or query, such as SQL, NoSQL, or OS command injection."},
    {"id": "A04:2021", "name": "Insecure Design",
     "summary": "Missing or ineffective security controls at the design stage, rather than a flaw in implementation."},
    {"id": "A05:2021", "name": "Security Misconfiguration",
     "summary": "Insecure default configurations, incomplete setups, open cloud storage, or overly verbose error messages."},
    {"id": "A06:2021", "name": "Vulnerable and Outdated Components",
     "summary": "Using libraries, frameworks, or other components with known vulnerabilities or that are no longer supported."},
    {"id": "A07:2021", "name": "Identification and Authentication Failures",
     "summary": "Weaknesses in confirming a user's identity, in authentication itself, or in session management."},
    {"id": "A08:2021", "name": "Software and Data Integrity Failures",
     "summary": "Code and infrastructure that doesn't protect against integrity violations, including insecure CI/CD pipelines and unsigned updates."},
    {"id": "A09:2021", "name": "Security Logging and Monitoring Failures",
     "summary": "Insufficient logging, detection, and alerting that delays or prevents timely detection of a breach."},
    {"id": "A10:2021", "name": "Server-Side Request Forgery (SSRF)",
     "summary": "An application fetches a remote resource without validating the user-supplied URL, letting an attacker reach internal-only systems."},
]


def main():
    documents = [
        {
            "source": "owasp",
            "title": f"{item['id']}: {item['name']}",
            "text": f"{item['name']} ({item['id']}). {item['summary']}",
            "metadata": {"category_id": item["id"]},
        }
        for item in OWASP_TOP_10
    ]
    count = ingest_documents(documents)
    print(f"Ingested {count} OWASP Top 10 categories into Qdrant")


if __name__ == "__main__":
    main()
