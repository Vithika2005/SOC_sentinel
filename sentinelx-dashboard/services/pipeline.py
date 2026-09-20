import requests


def get_pipeline_health(base_url):
    """
    Check the health of the SentinelX AI Orchestrator.
    """

    try:
        response = requests.get(
            f"{base_url}/health",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "available": True,
            "status": data.get("status", "ok"),
            "data": data
        }

    except requests.RequestException as error:

        return {
            "available": False,
            "status": "unavailable",
            "error": str(error)
        }


def run_pipeline(
    base_url,
    incident_ref,
    asset,
    source_type,
    severity,
    summary,
    timeout=180
):
    """
    Run the SentinelX LangGraph AI security pipeline.
    """

    payload = {
        "incident_ref": incident_ref,
        "asset": asset,
        "source_type": source_type,
        "severity": severity,
        "summary": summary
    }

    response = requests.post(
        f"{base_url}/pipeline/run",
        json=payload,
        timeout=timeout
    )

    response.raise_for_status()

    return response.json()