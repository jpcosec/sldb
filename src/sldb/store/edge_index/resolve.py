"""The rules that span documents, applied when the index is composed (they cannot live in a
shard: they depend on other documents): an authored edge inherits its type's condition and
axis and, if the type is undirected, gets its reverse; an authored edge to nothing is
reported and left out; a schema or alias edge to nothing is just left out. A RelationTypeDoc
is a `relation_type` node, not a document node, so an end written as its export id is first
moved onto that node."""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import RELATION_TYPE_MODEL, doc_node_id
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_DROPPED_IF_DANGLING = ("schema", "alias")


def relation_types_of(nodes: dict[str, EdgeNodeRecord]) -> dict[str, dict[str, Any]]:
    """Relation type name -> the payload of the RelationTypeDoc that declares it."""
    return {n.semantics.get("name", ""): n.semantics for n in nodes.values() if n.node_type == "relation_type"}


def resolve_edges(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord]) -> tuple[list[EdgeRecord], list[str]]:
    """(the edges that hold, the problems found with authored ones)."""
    relation_types = relation_types_of(nodes)
    edges = _onto_relation_type_nodes(nodes, edges)
    kept: list[EdgeRecord] = []
    problems: list[str] = []
    for e in edges:
        if e.metadata.get("origin") == "relation_doc":
            kept += _authored(e, nodes, relation_types.get(e.relation) or {}, problems)
        elif e.target in nodes or e.metadata.get("origin") not in _DROPPED_IF_DANGLING:
            kept.append(e)
    return kept, problems


def _authored(e: EdgeRecord, nodes: dict[str, EdgeNodeRecord], rt: dict[str, Any], problems: list[str]) -> list[EdgeRecord]:
    for end, node_id in (("source", e.source), ("target", e.target)):
        if node_id not in nodes:
            export_id = node_id[len("sldb://document/"):]
            problems.append(f"relation '{e.metadata.get('relation_doc')}': {end} '{export_id}' is not a tracked document")
            return []
    meta = {**e.metadata, "condition": e.metadata.get("condition") or rt.get("condition", ""), "axis": rt.get("axis", "")}
    forward = EdgeRecord(source=e.source, target=e.target, relation=e.relation, metadata=meta)
    if rt.get("direction") != "undirected":
        return [forward]
    return [forward, EdgeRecord(source=e.target, target=e.source, relation=e.relation, metadata={**meta, "reverse": True})]


def _onto_relation_type_nodes(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord]) -> list[EdgeRecord]:
    """Edges whose end is a RelationTypeDoc's export id, pointed at its `relation_type` node.

    A reference field holding `RelationTypeDoc:<doc>` names a tracked document, but the index
    holds that document as `sldb://relation_type/<payload name>`, so the edge used to dangle
    and be dropped in silence while `doc_exists` said the target was there.
    """
    moved = {doc_node_id(f"{RELATION_TYPE_MODEL}:{n.semantics['doc']}"): n.id for n in nodes.values() if n.node_type == "relation_type" and n.semantics.get("doc")}
    if not moved:
        return edges
    return [e.model_copy(update={"source": moved.get(e.source, e.source), "target": moved.get(e.target, e.target)}) for e in edges]
