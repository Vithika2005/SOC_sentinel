import plotly.graph_objects as go


def create_network_graph(graph_data):
    """
    Create a Plotly network graph from Neo4j relationships.
    """

    if not graph_data:
        return None

    nodes = {}

    for edge in graph_data:

        source = edge["source"]
        target = edge["target"]

        if source not in nodes:
            nodes[source] = len(nodes)

        if target not in nodes:
            nodes[target] = len(nodes)

    # Simple circular layout
    import math

    node_names = list(nodes.keys())
    node_count = len(node_names)

    positions = {}

    for index, node in enumerate(node_names):

        angle = (
            2 * math.pi * index / node_count
        )

        positions[node] = (
            math.cos(angle),
            math.sin(angle)
        )

    # ------------------------------------------
    # Relationship lines
    # ------------------------------------------

    edge_x = []
    edge_y = []

    for edge in graph_data:

        source = edge["source"]
        target = edge["target"]

        x1, y1 = positions[source]
        x2, y2 = positions[target]

        edge_x.extend([
            x1,
            x2,
            None
        ])

        edge_y.extend([
            y1,
            y2,
            None
        ])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        hoverinfo="none"
    )

    # ------------------------------------------
    # Nodes
    # ------------------------------------------

    node_x = []
    node_y = []
    node_text = []

    for node in node_names:

        x, y = positions[node]

        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            size=25
        )
    )

    # ------------------------------------------
    # Figure
    # ------------------------------------------

    fig = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    fig.update_layout(
        title="Neo4j Asset Relationship Graph",
        showlegend=False,
        hovermode="closest",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        )
    )

    return fig