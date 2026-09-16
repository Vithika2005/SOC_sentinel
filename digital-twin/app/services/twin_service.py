"""
STEP 14 -- Digital Twin.

Neo4j stores the enterprise topology as (:Asset)-[:CONNECTS_TO]->(:Asset).
Blast radius is computed as an actual graph algorithm, not a lookup table:

  1. direct_dependents    -- assets with an edge pointing AT this one (who calls it)
  2. direct_dependencies  -- assets this one points AT (what it calls)
  3. services_unreachable_if_isolated -- remove this node from the graph and
     see which assets that were reachable from the entrypoint (default:
     "Internet") no longer are. This is what catches "Database is only
     reachable through API" -- a single point of failure a flat dependency
     list would miss.
  4. affected_services = union of (1) and (3) -- your notes' example
     ("Database unavailable, 2 services affected") is exactly this union
     for a 3-hop chain.
"""
import networkx as nx

from app.core.neo4j_client import neo4j_db


class AssetNotFoundError(Exception):
    pass


def seed_topology(edges: list[tuple[str, str, str, str]]) -> int:
    """edges: list of (source, source_type, target, target_type)."""
    query = """
    UNWIND $edges AS edge
    MERGE (a:Asset {name: edge.source})
      ON CREATE SET a.type = edge.source_type
    MERGE (b:Asset {name: edge.target})
      ON CREATE SET b.type = edge.target_type
    MERGE (a)-[:CONNECTS_TO]->(b)
    """
    payload = [
        {"source": s, "source_type": st, "target": t, "target_type": tt}
        for s, st, t, tt in edges
    ]
    with neo4j_db.driver.session() as session:
        session.run(query, edges=payload)
    return len(edges)


def get_graph() -> nx.DiGraph:
    query = """
    MATCH (a:Asset)-[:CONNECTS_TO]->(b:Asset)
    RETURN a.name AS source, a.type AS source_type, b.name AS target, b.type AS target_type
    """
    graph = nx.DiGraph()
    with neo4j_db.driver.session() as session:
        result = session.run(query)
        for record in result:
            graph.add_node(record["source"], type=record["source_type"])
            graph.add_node(record["target"], type=record["target_type"])
            graph.add_edge(record["source"], record["target"])
    return graph


def compute_blast_radius(asset: str, entrypoint: str) -> dict:
    graph = get_graph()
    if asset not in graph:
        raise AssetNotFoundError(asset)

    direct_dependents = sorted(graph.predecessors(asset))
    direct_dependencies = sorted(graph.successors(asset))

    if entrypoint in graph:
        baseline_reachable = nx.descendants(graph, entrypoint) | {entrypoint}
    else:
        baseline_reachable = set(graph.nodes())

    graph_without = graph.copy()
    graph_without.remove_node(asset)

    if entrypoint in graph_without:
        reachable_without = nx.descendants(graph_without, entrypoint) | {entrypoint}
    else:
        reachable_without = set()

    unreachable = sorted((baseline_reachable - reachable_without) - {asset})
    affected_services = sorted(set(direct_dependents) | set(unreachable))

    return {
        "asset": asset,
        "entrypoint": entrypoint,
        "direct_dependents": direct_dependents,
        "direct_dependencies": direct_dependencies,
        "services_unreachable_if_isolated": unreachable,
        "affected_services": affected_services,
        "affected_count": len(affected_services),
    }


def get_graph_summary() -> dict:
    graph = get_graph()
    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "nodes": sorted(graph.nodes()),
    }
