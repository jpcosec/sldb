"""The composed edge index: every node and edge of a store (and its linked stores), in memory."""

from __future__ import annotations

from pydantic import BaseModel, Field, PrivateAttr

from sldb.store.edge_index.node_ids import as_node_id
from sldb.store.models import EdgeNodeRecord, EdgeRecord


class EdgeIndex(BaseModel):
    """What the shards say, composed: the one door for reading edges. Ids are node ids
    (`sldb://document/Model:name`...); a bare export id `Model:name` is read as its document's."""

    nodes: dict[str, EdgeNodeRecord] = Field(default_factory=dict, description="Every node by id; the same id contributed twice is one node.")
    edges: list[EdgeRecord] = Field(default_factory=list, description="Every edge, cross-document rules applied (inherited conditions, reverse edges, edges to nothing dropped).")
    problems: list[str] = Field(default_factory=list, description="Authored edges left out because an endpoint is not a node; reported, never stored.")
    stale: list[str] = Field(default_factory=list, description="Export ids of tracked documents whose shard is missing or built from another hash_c: run the rebuild.")
    _out: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)
    _in: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)

    def edges_from(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges leaving `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._out or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def edges_to(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges pointing at `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._in or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def node(self, node_id: str) -> EdgeNodeRecord | None:
        """The node with that id (or that export id), None when the index has none."""
        return self.nodes.get(as_node_id(node_id))

    def nodes_of_type(self, node_type: str) -> list[EdgeNodeRecord]:
        """Nodes of one class, sorted by id; a document's class is its model's name."""
        return sorted((n for n in self.nodes.values() if n.node_type == node_type), key=lambda n: n.id)

    def _ensure_maps(self) -> None:
        if self._out is not None:
            return
        self._out, self._in = {}, {}
        for e in self.edges:
            self._out.setdefault(e.source, []).append(e)
            self._in.setdefault(e.target, []).append(e)
