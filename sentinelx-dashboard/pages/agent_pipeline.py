import streamlit as st
from config import AI_ORCHESTRATOR_URL
from services.pipeline import get_pipeline_health


st.title("AI Agent Pipeline")

st.write(
    "SentinelX uses a multi-agent AI pipeline for incident investigation. "
    "The pipeline is executed by the AI Orchestrator service."
)

st.info(
    "Pipeline execution is intentionally not triggered from the dashboard "
    "because the multi-agent workflow can take several minutes to complete."
)

st.subheader("AI Orchestrator Status")

if st.button("Check Pipeline Health"):
    try:
        result = get_pipeline_health(AI_ORCHESTRATOR_URL)

        if result.get("available"):
            st.success(
                f"AI Orchestrator is available — "
                f"Status: {result.get('status', 'ok')}"
            )

            with st.expander("Service Response"):
                st.json(result.get("data", {}))
        else:
            st.error("AI Orchestrator is unavailable.")

            if result.get("error"):
                st.code(result["error"])

    except Exception as error:
        st.error(f"Unable to check AI Orchestrator: {error}")


st.subheader("Pipeline Architecture")

st.markdown(
    """
    **Incident**
    
    ↓
    
    **Recon Agent**
    
    ↓
    
    **Threat Intelligence Agent**
    
    ↓
    
    **Risk Agent**
    
    ↓
    
    **Decision Agent**
    
    ↓
    
    **Auditor Agent**
    
    ↓
    
    **Investigation Result**
    """
)

st.caption(
    "The AI pipeline can still be executed directly through the "
    "AI Orchestrator API when required."
)