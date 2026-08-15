from typing import Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    source_filter: Optional[str] = None  # "mitre" | "owasp" | "playbook"


class SearchHit(BaseModel):
    score: float
    source: str
    title: str
    text: str
    metadata: dict = {}


class SearchResponse(BaseModel):
    query: str
    hits: list[SearchHit]


class IngestDocument(BaseModel):
    source: str
    title: str
    text: str
    metadata: dict = {}


class IngestRequest(BaseModel):
    documents: list[IngestDocument]
