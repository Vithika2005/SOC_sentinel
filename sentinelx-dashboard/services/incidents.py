import requests
import pandas as pd


def get_incidents(base_url, status=None, limit=50, offset=0):
    params = {
        "limit": limit,
        "offset": offset,
    }

    if status:
        params["status"] = status

    response = requests.get(
        f"{base_url}/incidents",
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.json_normalize(data)


def get_dashboard_stats(base_url):
    response = requests.get(
        f"{base_url}/incidents/dashboard/stats",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_incident(base_url, incident_id):
    response = requests.get(
        f"{base_url}/incidents/{incident_id}",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_incident_summary(df):
    if df.empty:
        return {
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

    summary = {
        "total": len(df),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    if "severity" in df.columns:
        severity = (
            df["severity"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        for level in ["critical", "high", "medium", "low"]:
            summary[level] = int(
                (severity == level).sum()
            )

    return summary