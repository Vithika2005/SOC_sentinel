import json
from pathlib import Path

import pandas as pd


def load_findings(file_path):
    """
    Load SentinelX security findings from JSON.

    Returns:
        pandas.DataFrame
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Findings file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Handle common JSON structures
    if isinstance(data, list):
        findings = data

    elif isinstance(data, dict):
        if "findings" in data:
            findings = data["findings"]

        elif "results" in data:
            findings = data["results"]

        else:
            findings = [data]

    else:
        raise ValueError(
            "Unsupported findings JSON format."
        )

    return pd.json_normalize(findings)


def get_finding_summary(df):
    """
    Return basic statistics for the dashboard.
    """

    if df.empty:
        return {
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

    severity_column = None

    for column in ["severity", "Severity", "level", "priority"]:
        if column in df.columns:
            severity_column = column
            break

    if severity_column is None:
        return {
            "total": len(df),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

    severity = (
        df[severity_column]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    return {
        "total": len(df),
        "critical": int((severity == "critical").sum()),
        "high": int((severity == "high").sum()),
        "medium": int((severity == "medium").sum()),
        "low": int((severity == "low").sum()),
    }