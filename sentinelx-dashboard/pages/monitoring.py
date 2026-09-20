import streamlit as st
import pandas as pd

from config import PROMETHEUS_URL, GRAFANA_URL
from services.monitoring import (
    get_service_health,
    get_service_response_time,
    get_qdrant_vector_count,
    get_monitoring_components,
)


st.set_page_config(
    page_title="SentinelX Monitoring",
    page_icon="📊",
    layout="wide",
)


st.title("SentinelX Monitoring")

st.caption(
    "Live infrastructure and service monitoring powered by Prometheus."
)


# ---------------------------------------------------------
# Fetch monitoring data
# ---------------------------------------------------------

services = get_service_health(PROMETHEUS_URL)

response_times = get_service_response_time(PROMETHEUS_URL)

qdrant_vectors = get_qdrant_vector_count(PROMETHEUS_URL)

monitoring_components = get_monitoring_components(PROMETHEUS_URL)


# ---------------------------------------------------------
# Top metrics
# ---------------------------------------------------------

up_count = sum(
    1 for service in services
    if service["status"] == "UP"
)

down_count = sum(
    1 for service in services
    if service["status"] == "DOWN"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Services UP",
        up_count,
    )

with col2:
    st.metric(
        "Services DOWN",
        down_count,
    )

with col3:
    st.metric(
        "Threat Intel Vectors",
        qdrant_vectors if qdrant_vectors is not None else "N/A",
    )

with col4:
    st.metric(
        "Monitored Services",
        len(services),
    )


st.divider()


# ---------------------------------------------------------
# Service Health
# ---------------------------------------------------------

st.subheader("Service Health")

if services:

    service_df = pd.DataFrame(services)

    st.dataframe(
        service_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "No service health data is currently available from Prometheus."
    )


# ---------------------------------------------------------
# Response Time
# ---------------------------------------------------------

st.subheader("HTTP Response Time")

if response_times:

    response_df = pd.DataFrame(response_times)

    response_df = response_df.sort_values(
        "response_time_ms",
        ascending=False,
    )

    st.bar_chart(
        response_df.set_index("service")[
            "response_time_ms"
        ]
    )

else:

    st.info(
        "No response-time data is currently available."
    )


# ---------------------------------------------------------
# Monitoring Components
# ---------------------------------------------------------

st.subheader("Monitoring Components")

if monitoring_components:

    component_df = pd.DataFrame(
        monitoring_components
    )

    st.dataframe(
        component_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Prometheus monitoring component data is unavailable."
    )


# ---------------------------------------------------------
# Qdrant
# ---------------------------------------------------------

st.subheader("Threat Intelligence")

if qdrant_vectors is not None:

    st.write(
        f"Qdrant collection `threat-intel` currently contains "
        f"**{qdrant_vectors:,} vectors**."
    )

else:

    st.warning(
        "Unable to retrieve Qdrant vector count."
    )


# ---------------------------------------------------------
# Grafana
# ---------------------------------------------------------

st.divider()

st.subheader("Detailed Monitoring")

st.write(
    "Grafana provides the detailed operational monitoring "
    "view for SentinelX."
)

st.link_button(
    "Open SentinelX Grafana Dashboard",
    GRAFANA_URL,
)