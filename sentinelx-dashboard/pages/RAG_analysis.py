import streamlit as st
import pandas as pd
import plotly.express as px

from config import RAG_SERVICE_URL
from services.rag import (
    get_rag_stats,
    search_rag
)

st.set_page_config(
    page_title="RAG Analysis | SentinelX",
    page_icon="🧠",
    layout="wide"
)

st.title("RAG Analysis")

st.caption(
    "Retrieval-Augmented Generation, document retrieval and similarity scoring."
)


# --------------------------------------------------
# RAG service status
# --------------------------------------------------

try:

    rag_stats = get_rag_stats(
        RAG_SERVICE_URL
    )

    st.success("RAG Service Connected")

except Exception as error:

    st.error(
        f"Unable to connect to RAG Service: {error}"
    )

    rag_stats = None


# --------------------------------------------------
# RAG statistics
# --------------------------------------------------

if rag_stats:

    st.subheader("RAG Knowledge Base")

    st.json(rag_stats)


st.divider()


# --------------------------------------------------
# Search
# --------------------------------------------------

st.subheader("RAG Search")

query = st.text_area(
    "Enter a security question or search query",
    value="Terraform password security finding",
    height=100
)

col1, col2 = st.columns(2)

with col1:

    top_k = st.number_input(
        "Number of Results",
        min_value=1,
        max_value=20,
        value=5
    )

with col2:

    source_filter = st.text_input(
        "Source Filter (optional)",
        placeholder="e.g. Secrets"
    )


if st.button(
    "Search Knowledge Base",
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Searching SentinelX knowledge base..."
        ):

            try:

                result = search_rag(
                    RAG_SERVICE_URL,
                    query,
                    top_k=int(top_k),
                    source_filter=source_filter.strip()
                    if source_filter.strip()
                    else None
                )

                st.session_state["rag_result"] = result

            except Exception as error:

                st.error(
                    f"RAG search failed: {error}"
                )


# --------------------------------------------------
# Results
# --------------------------------------------------

if "rag_result" in st.session_state:

    result = st.session_state["rag_result"]

    st.divider()

    st.subheader("Retrieved Results")

    hits = result.get("hits", [])

    if not hits:

        st.info(
            "The RAG service returned no matching documents."
        )

    else:

        # ------------------------------------------
        # Score metrics
        # ------------------------------------------

        scores = [
            float(hit.get("score", 0))
            for hit in hits
        ]

        avg_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        max_score = max(scores) if scores else 0

        min_score = min(scores) if scores else 0


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Results Retrieved",
                len(hits)
            )

        with col2:

            st.metric(
                "Best RAG Score",
                f"{max_score:.4f}"
            )

        with col3:

            st.metric(
                "Average RAG Score",
                f"{avg_score:.4f}"
            )


        st.divider()


        # ------------------------------------------
        # Score chart
        # ------------------------------------------

        score_df = pd.DataFrame({
            "Result": [
                f"Result {i + 1}"
                for i in range(len(hits))
            ],
            "Score": scores
        })

        fig = px.bar(
            score_df,
            x="Result",
            y="Score",
            title="RAG Retrieval Scores"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ------------------------------------------
        # Individual results
        # ------------------------------------------

        for index, hit in enumerate(hits):

            score = hit.get("score", 0)

            title = hit.get(
                "title",
                "Untitled"
            )

            source = hit.get(
                "source",
                "Unknown"
            )

            text = hit.get(
                "text",
                ""
            )

            metadata = hit.get(
                "metadata",
                {}
            )


            with st.expander(
                f"Result {index + 1} — "
                f"Score: {float(score):.4f}"
            ):

                st.markdown(
                    f"**Title:** {title}"
                )

                st.markdown(
                    f"**Source:** {source}"
                )

                st.markdown(
                    f"**Similarity Score:** `{float(score):.4f}`"
                )

                st.markdown("### Retrieved Text")

                st.write(text)

                if metadata:

                    st.markdown("### Metadata")

                    st.json(metadata)