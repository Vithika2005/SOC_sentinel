from pydantic import BaseModel


class Edge(BaseModel):
    source: str
    source_type: str = "service"
    target: str
    target_type: str = "service"


class SeedRequest(BaseModel):
    edges: list[Edge]


class BlastRadiusResponse(BaseModel):
    asset: str
    entrypoint: str
    direct_dependents: list[str]      # who calls this asset directly
    direct_dependencies: list[str]    # what this asset calls directly
    services_unreachable_if_isolated: list[str]  # lose ALL paths from entrypoint if this asset is removed
    affected_services: list[str]      # union of the above -- the actual blast radius
    affected_count: int


class GraphSummary(BaseModel):
    node_count: int
    edge_count: int
    nodes: list[str]
