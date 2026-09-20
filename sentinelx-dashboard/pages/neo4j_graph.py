import streamlit as st
import pandas as pd

from config import (
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)

from services.neo4j import (
    test_connection,
    get_node_summary,
    get_relationship_summary,
    get_graph_data
)

from components.graph import create_network_graph


st.set_page_config(
    page_title="Neo4j Graph | SentinelX",
    page_icon="🕸️",
    layout="wide"
)


st.title("Neo4j Graph")

st.caption(
    "Live asset relationships stored in the SentinelX Neo4j knowledge graph."
)


# --------------------------------------------------
# Connection
# --------------------------------------------------

try:

    connected = test_connection(
        NEO4J_URI,
        NEO4J_USER,
        NEO4J_PASSWORD
    )

    if connected:
        st.success(
            "Neo4j Connected"
        )

except Exception as error:

    st.error(
        f"Neo4j connection failed: {error}"
    )

    st.stop()


# --------------------------------------------------
# Node summary
# --------------------------------------------------

node_summary = get_node_summary(
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)

relationship_summary = get_relationship_summary(
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)


total_nodes = sum(
    item["count"]
    for item in node_summary
)

total_relationships = sum(
    item["count"]
    for item in relationship_summary
)


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Nodes",
        total_nodes
    )

with col2:

    st.metric(
        "Total Relationships",
        total_relationships
    )


st.divider()


# --------------------------------------------------
# Actual graph
# --------------------------------------------------

st.subheader(
    "🔗 Asset Relationship Graph"
)

graph_data = get_graph_data(
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)


if graph_data:

    fig = create_network_graph(
        graph_data
    )

    if fig:

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Neo4j currently contains no relationships."
    )


# --------------------------------------------------
# Node information
# --------------------------------------------------

st.divider()

st.subheader(
    "Node Summary"
)

if node_summary:

    node_df = pd.DataFrame(
        node_summary
    )

    node_df["labels"] = (
        node_df["labels"]
        .apply(
            lambda x: ", ".join(x)
            if isinstance(x, list)
            else str(x)
        )
    )

    st.dataframe(
        node_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Relationship information
# --------------------------------------------------

st.subheader(
    "Relationship Types"
)

if relationship_summary:

    relationship_df = pd.DataFrame(
        relationship_summary
    )

    st.dataframe(
        relationship_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Raw relationships
# --------------------------------------------------

with st.expander(
    "View Actual Neo4j Relationships"
):

    if graph_data:

        st.dataframe(
            pd.DataFrame(graph_data),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No relationships found."
        )