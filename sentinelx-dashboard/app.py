# sentinelx-dashboard/app.py

import streamlit as st

from config import FINDINGS_FILE
from services.findings import (
    load_findings,
    get_finding_summary
)


st.set_page_config(
    page_title="SentinelX SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("SentinelX")

st.sidebar.caption(
    "Security Operations Dashboard"
)

st.sidebar.divider()

st.sidebar.markdown(
    """
### Navigation

Overview

Security Findings

Incidents

Agent Pipeline

Digital Twin

RAG Analysis

Neo4j Graph

Infrastructure
"""
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("SentinelX SOC Dashboard")

st.markdown(
    """
### Security Operations Overview

Monitor security findings, incidents, AI-agent execution,
Digital Twin relationships, RAG retrieval, Neo4j knowledge
graphs and infrastructure dependencies from one dashboard.
"""
)


# ---------------------------------------------------------
# Load findings
# ---------------------------------------------------------

try:

    findings_df = load_findings(
        FINDINGS_FILE
    )

    summary = get_finding_summary(
        findings_df
    )

except Exception as error:

    st.error(
        f"Unable to load SentinelX findings: {error}"
    )

    findings_df = None

    summary = {
        "total": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }


# ---------------------------------------------------------
# Top metrics
# ---------------------------------------------------------

st.subheader("Security Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Security Findings",
        summary["total"]
    )

with col2:
    st.metric(
        "Critical Findings",
        summary["critical"]
    )

with col3:
    st.metric(
        "High Findings",
        summary["high"]
    )

with col4:
    st.metric(
        "Medium Findings",
        summary["medium"]
    )


st.divider()


# ---------------------------------------------------------
# System architecture
# ---------------------------------------------------------

st.subheader("SentinelX Processing Pipeline")

st.code(
    """
Security Findings
        │
        ▼
      Kafka
        │
        ▼
 Incident Service
        │
        ▼
  LangGraph Agents
        │
   ┌────┼─────┐
   ▼    ▼     ▼
 Recon  RAG   Risk
   │    │     │
   └────┼─────┘
        ▼
    Decision
        │
        ▼
     Auditor
        │
        ▼
 Recommendation
        │
   ┌────┴────┐
   ▼         ▼
Digital     Neo4j
 Twin       Graph
    """,
    language="text"
)


st.divider()


# ---------------------------------------------------------
# Current data source
# ---------------------------------------------------------

st.subheader("Connected Data Sources")

source_col1, source_col2, source_col3 = st.columns(3)

with source_col1:
    st.success("Security Findings")
    st.caption("sentinelx_findings.json")

with source_col2:
    st.info("Kafka / Incidents")
    st.caption("Integration coming next")

with source_col3:
    st.info("LangGraph Pipeline")
    st.caption("Integration coming next")


st.info(
    "Use the pages in the sidebar to explore individual "
    "SentinelX components."
)