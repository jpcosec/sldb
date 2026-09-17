"""What one contributor (a document, a model, the store) adds to the edge index."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord


class EdgeContribution(BaseModel):
    """Nodes and edges of one contributor; also the store-level shard's own shape."""

    edges_version: str = Field(default="", description="EDGE_INDEX_VERSION the contribution was built under; a new rule rebuilds it.")
    nodes: list[EdgeNodeRecord] = Field(default_factory=list, description="Nodes this contributor brings; the same id from two contributors is one node.")
    edges: list[EdgeRecord] = Field(default_factory=list, description="Edges this contributor brings, whatever node they leave from.")
