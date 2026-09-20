# sentinelx-dashboard/components/metrics.py

import streamlit as st


def show_metric(label, value, description=None):
    """
    Display a single SentinelX metric.
    """

    st.metric(
        label=label,
        value=value,
        help=description
    )


def show_metrics(metrics):
    """
    Display multiple metrics.

    Example:
        show_metrics({
            "Security Findings": 121,
            "Incidents": 25,
            "Containers": 12
        })
    """

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(columns, metrics.items()):
        with column:
            st.metric(
                label=label,
                value=value
            )