import streamlit as st

from config import INCIDENT_SERVICE_URL
from services.incidents import (
    get_incidents,
    get_dashboard_stats,
)

st.set_page_config(
    page_title="Incidents | SentinelX",
    page_icon="🚨",
    layout="wide"
)

st.title("Incidents")

st.caption(
    "Live incident records from the SentinelX Incident Service."
)


# --------------------------------------------------
# Refresh
# --------------------------------------------------

if st.button("Refresh Incidents"):
    st.rerun()


# --------------------------------------------------
# Dashboard statistics
# --------------------------------------------------

try:
    stats = get_dashboard_stats(
        INCIDENT_SERVICE_URL
    )

except Exception as error:
    st.error(
        f"Unable to load incident statistics: {error}"
    )
    stats = None


if stats:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Incidents",
            stats.get("total_incidents", 0)
        )

    with col2:
        st.metric(
            "Open Incidents",
            stats.get("open_incidents", 0)
        )

    with col3:
        st.metric(
            "Critical Incidents",
            stats.get("critical_incidents", 0)
        )

    with col4:
        st.metric(
            "Last 24 Hours",
            stats.get("incidents_last_24h", 0)
        )


st.divider()


# --------------------------------------------------
# Incident records
# --------------------------------------------------

st.subheader("Incident Records")

try:

    incidents_df = get_incidents(
        INCIDENT_SERVICE_URL,
        limit=200
    )

except Exception as error:

    st.error(
        f"Unable to load incidents: {error}"
    )

    st.stop()


if incidents_df.empty:

    st.info(
        "No incident records are currently available."
    )

else:

    # --------------------------------------------------
    # Filters
    # --------------------------------------------------

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        if "severity" in incidents_df.columns:

            severity_options = ["All"] + sorted(
                incidents_df["severity"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_severity = st.selectbox(
                "Filter by Severity",
                severity_options
            )

        else:

            selected_severity = "All"


    with filter_col2:

        if "status" in incidents_df.columns:

            status_options = ["All"] + sorted(
                incidents_df["status"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_status = st.selectbox(
                "Filter by Status",
                status_options
            )

        else:

            selected_status = "All"


    # --------------------------------------------------
    # Apply filters
    # --------------------------------------------------

    filtered_df = incidents_df.copy()


    if (
        selected_severity != "All"
        and "severity" in filtered_df.columns
    ):

        filtered_df = filtered_df[
            filtered_df["severity"].astype(str)
            == selected_severity
        ]


    if (
        selected_status != "All"
        and "status" in filtered_df.columns
    ):

        filtered_df = filtered_df[
            filtered_df["status"].astype(str)
            == selected_status
        ]


    st.write(
        f"Showing **{len(filtered_df)}** incident(s)"
    )


    # --------------------------------------------------
    # Incident table
    # --------------------------------------------------

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Incident Analysis
# --------------------------------------------------

st.divider()

st.subheader("Incident Analysis")

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    if (
        not incidents_df.empty
        and "severity" in incidents_df.columns
    ):

        severity_counts = (
            incidents_df["severity"]
            .fillna("Unknown")
            .astype(str)
            .str.upper()
            .value_counts()
        )

        st.bar_chart(
            severity_counts,
            x_label="Severity",
            y_label="Incidents"
        )

    else:

        st.info(
            "Severity information is not available."
        )


with chart_col2:

    if (
        not incidents_df.empty
        and "status" in incidents_df.columns
    ):

        status_counts = (
            incidents_df["status"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        st.bar_chart(
            status_counts,
            x_label="Status",
            y_label="Incidents"
        )

    else:

        st.info(
            "Status information is not available."
        )


# --------------------------------------------------
# Bloom Filter
# --------------------------------------------------

st.divider()

st.subheader("Bloom Filter")

st.caption(
    "The Incident Service uses an in-memory Bloom Filter "
    "as a fast probabilistic pre-check for alert deduplication."
)


bloom_col1, bloom_col2, bloom_col3, bloom_col4 = st.columns(4)


with bloom_col1:
    st.metric(
        "Capacity",
        "100,000"
    )


with bloom_col2:
    st.metric(
        "Configured Error Rate",
        "0.001"
    )


with bloom_col3:
    st.metric(
        "Hash Algorithm",
        "SHA-256"
    )


with bloom_col4:
    st.metric(
        "Storage",
        "In-memory"
    )


st.info(
    "The current Incident Service does not expose the Bloom Filter's "
    "live bit-array state or inserted-item count through an API. "
    "Therefore, the dashboard displays only the configured properties "
    "of the Bloom Filter and does not fabricate a live item count."
)