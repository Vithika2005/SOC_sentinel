import streamlit as st
import docker

st.set_page_config(
    page_title="Infrastructure | SentinelX",
    page_icon="🐳",
    layout="wide"
)

st.title("Infrastructure")

st.caption(
    "Docker containers and infrastructure dependencies used by SentinelX."
)

try:

    client = docker.from_env()

    client.ping()

    st.success("Docker Engine connected")

except Exception as error:

    st.error(
        f"Unable to connect to Docker: {error}"
    )

    st.stop()


containers = client.containers.list(
    all=True
)

st.subheader("Container Overview")

running = 0
stopped = 0

for container in containers:

    status = container.status

    if status == "running":
        running += 1
    else:
        stopped += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Containers",
        len(containers)
    )

with col2:
    st.metric(
        "Running",
        running
    )

with col3:
    st.metric(
        "Stopped",
        stopped
    )

st.divider()

rows = []

for container in containers:

    rows.append({
        "Name": container.name,
        "Status": container.status,
        "Image": container.image.tags[0]
        if container.image.tags
        else container.image.short_id,
        "Container ID": container.short_id
    })

st.subheader("Docker Containers")

if rows:

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Docker containers found.")