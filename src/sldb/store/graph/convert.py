"""Conversions between the edge index and the portable GraphSnapshot."""

from __future__ import annotations

from sldb.store.graph.edge import Edge
from sldb.store.graph.facet import FacetPayload
from sldb.store.graph.identity import SystemIdentity
from sldb.store.graph.node import KnowledgeNode
from sldb.store.graph.snapshot import GraphSnapshot
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def snapshot_from_index(index: EdgeIndex) -> GraphSnapshot:
    """Build a GraphSnapshot from an edge index: every node, its outgoing edges."""
    nodes = [_knowledge_node(index, node) for node in sorted(index.nodes.values(), key=lambda n: n.id)]
    return GraphSnapshot(version="1.0", nodes=nodes, metadata={"generated_from": "sldb.store.edge_index"})


def index_from_snapshot(snapshot: GraphSnapshot) -> EdgeIndex:
    """Build an EdgeIndex from a snapshot: every node and edge as the shards would hold them."""
    nodes = {n.identity.node_id: _record(n) for n in snapshot.nodes}
    edges = [_record_edge(n.identity.node_id, e) for n in snapshot.nodes for e in n.edges]
    return EdgeIndex(nodes=nodes, edges=edges)


def _knowledge_node(index: EdgeIndex, node: EdgeNodeRecord) -> KnowledgeNode:
    return KnowledgeNode(
        identity=SystemIdentity(node_id=node.id, node_type=node.node_type),
        edges=[Edge(target_id=e.target, relation_type=e.relation, metadata=e.metadata) for e in index.edges_from(node.id)],
        semantics=_facet(node.semantics),
        git=_facet(node.facets.get("git")),
        source=_facet(node.facets.get("source")),
    )


def _record(node: KnowledgeNode) -> EdgeNodeRecord:
    return EdgeNodeRecord(id=node.identity.node_id, node_type=node.identity.node_type, semantics=_dump(node.semantics), facets=_facets(node))


def _record_edge(source: str, edge: Edge) -> EdgeRecord:
    return EdgeRecord(source=source, target=edge.target_id, relation=edge.relation_type, metadata=edge.metadata)


def _facet(payload):
    if not payload:
        return None
    return FacetPayload.model_validate(payload)


def _dump(payload) -> dict:
    return {} if payload is None else payload.model_dump()


def _facets(node: KnowledgeNode) -> dict:
    facets = {}
    if node.git is not None:
        facets["git"] = node.git.model_dump()
    if node.source is not None:
        facets["source"] = node.source.model_dump()
    return facets
