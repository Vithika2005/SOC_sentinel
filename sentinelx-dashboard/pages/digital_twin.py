import streamlit as st

from config import DIGITAL_TWIN_URL
from services.digital_twin import (
    get_graph,
    get_blast_radius,
    get_health
)

st.set_page_config(
    page_title="Digital Twin | SentinelX",
    page_icon="🌐",
    layout="wide"
)

st.title("Digital Twin")

st.caption(
    "Enterprise topology, dependencies and blast-radius analysis."
)


# --------------------------------------------------
# Health
# --------------------------------------------------

try:

    health = get_health(
        DIGITAL_TWIN_URL
    )

    st.success(
        f"Digital Twin connected — {health}"
    )

except Exception as error:

    st.error(
        f"Digital Twin connection failed: {error}"
    )

    st.stop()


# --------------------------------------------------
# Graph Summary
# --------------------------------------------------

st.subheader("🕸️ Digital Twin Graph")

try:

    graph = get_graph(
        DIGITAL_TWIN_URL
    )

except Exception as error:

    st.error(
        f"Unable to load Digital Twin graph: {error}"
    )

    graph = None


if graph:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Nodes",
            graph.get("node_count", 0)
        )

    with col2:

        st.metric(
            "Edges",
            graph.get("edge_count", 0)
        )


    st.divider()

    st.subheader("Assets / Nodes")

    nodes = graph.get("nodes", [])

    if nodes:

        for node in nodes:

            st.write(
                f"🔹 {node}"
            )

    else:

        st.info(
            "No Digital Twin nodes returned."
        )


# --------------------------------------------------
# Blast Radius
# --------------------------------------------------

st.divider()

st.subheader("Blast Radius Analysis")

asset = st.text_input(
    "Asset",
    value="auth-service"
)

entrypoint = st.text_input(
    "Entrypoint (optional)",
    placeholder="Leave empty to use service default"
)


if st.button(
    "Calculate Blast Radius",
    type="primary"
):

    try:

        result = get_blast_radius(
            DIGITAL_TWIN_URL,
            asset,
            entrypoint.strip()
            if entrypoint.strip()
            else None
        )

        st.session_state[
            "blast_radius"
        ] = result

    except Exception as error:

        st.error(
            f"Blast radius calculation failed: {error}"
        )


if "blast_radius" in st.session_state:

    result = st.session_state[
        "blast_radius"
    ]

    st.divider()

    st.subheader(
        f"Blast Radius — {result.get('asset', asset)}"
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Affected Services",
            result.get("affected_count", 0)
        )

    with col2:

        st.metric(
            "Direct Dependencies",
            len(
                result.get(
                    "direct_dependencies",
                    []
                )
            )
        )

    with col3:

        st.metric(
            "Direct Dependents",
            len(
                result.get(
                    "direct_dependents",
                    []
                )
            )
        )


    affected = result.get(
        "affected_services",
        []
    )

    if affected:

        st.subheader(
            "Affected Services"
        )

        for service in affected:

            st.write(
                f"{service}"
            )


    dependencies = result.get(
        "direct_dependencies",
        []
    )

    if dependencies:

        st.subheader(
            "Direct Dependencies"
        )

        for dependency in dependencies:

            st.write(
                f"{dependency}"
            )


    dependents = result.get(
        "direct_dependents",
        []
    )

    if dependents:

        st.subheader(
            "Direct Dependents"
        )

        for dependent in dependents:

            st.write(
                f"{dependent}"
            )


    with st.expander(
        "View Complete Blast-Radius Response"
    ):

        st.json(result)