# sentinelx-dashboard/pages/02_Security_Findings.py

import streamlit as st

from config import FINDINGS_FILE
from services.findings import (
    load_findings,
    get_finding_summary
)
from components.charts import (
    severity_chart,
    category_chart
)


st.set_page_config(
    page_title="Security Findings | SentinelX",
    page_icon="🔐",
    layout="wide"
)


st.title("Security Findings")

st.caption(
    "Security findings collected from SentinelX DevSecOps analysis."
)


# ---------------------------------------------------------
# Load findings
# ---------------------------------------------------------

try:
    findings_df = load_findings(FINDINGS_FILE)

except Exception as error:
    st.error(f"Unable to load findings: {error}")
    st.stop()


summary = get_finding_summary(findings_df)


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Findings",
        summary["total"]
    )

with col2:
    st.metric(
        "Critical",
        summary["critical"]
    )

with col3:
    st.metric(
        "High",
        summary["high"]
    )

with col4:
    st.metric(
        "Medium",
        summary["medium"]
    )

with col5:
    st.metric(
        "Low",
        summary["low"]
    )


st.divider()


# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)


with left:

    severity_fig = severity_chart(findings_df)

    if severity_fig:
        st.plotly_chart(
            severity_fig,
            use_container_width=True
        )
    else:
        st.info(
            "Severity information is not available."
        )


with right:

    # Find whichever category field exists
    category_column = None

    for column in [
        "type",
        "category",
        "finding_type",
        "tool"
    ]:
        if column in findings_df.columns:
            category_column = column
            break

    if category_column:

        category_fig = category_chart(
            findings_df,
            category_column
        )

        if category_fig:
            st.plotly_chart(
                category_fig,
                use_container_width=True
            )

    else:
        st.info(
            "Finding category information is not available."
        )


st.divider()


# ---------------------------------------------------------
# Raw findings table
# ---------------------------------------------------------

st.subheader("Finding Records")

st.dataframe(
    findings_df,
    use_container_width=True,
    hide_index=True
)