"""Every edge checked against its relation type (kgdb's TypedIngestError, as a report): the
type is a tracked RelationTypeDoc, the target exists, both endpoint classes are allowed (model
names inherit through `base_models`), and cardinality holds."""

from __future__ import annotations

from collections import Counter
from typing import Any

from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.resolve import relation_types_of
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_BUILTIN_ORIGINS = ("structural", "schema", "alias")


def validate_edge_index(index: EdgeIndex) -> list[str]:
    """The violations found, as sentences; empty when every edge is valid."""
    relation_types = relation_types_of(index.nodes)
    errors: list[str] = []
    for e in index.edges:
        errors += _edge_errors(index.nodes, e, relation_types.get(e.relation))
    return errors + _cardinality_errors(index.edges, relation_types)


def _edge_errors(nodes: dict[str, EdgeNodeRecord], e: EdgeRecord, rt: dict[str, Any] | None) -> list[str]:
    where = f"edge {e.source} -[{e.relation}]-> {e.target}"
    if rt is None:
        hint = " (run `sldb edges init` to track the builtin relation types)" if e.metadata.get("origin") in _BUILTIN_ORIGINS else ""
        return [f"{where}: unknown relation type '{e.relation}'{hint}"]
    if e.target not in nodes or e.source not in nodes:
        return [f"{where}: target does not exist"]
    ends = (("source", nodes[e.source], rt.get("source_types") or []), ("target", nodes[e.target], rt.get("target_types") or []))
    return [f"{where}: {end} class '{node.node_type}' not in {end}_types {allowed}" for end, node, allowed in ends if not _class_ok(nodes, node, allowed)]


def _class_ok(nodes: dict[str, EdgeNodeRecord], node: EdgeNodeRecord, allowed: list[str]) -> bool:
    model = nodes.get(f"sldb://model/{node.node_type}")
    if not allowed or ("sldb_document" in allowed and model is not None):
        return True
    lineage = [node.node_type] + list(model.semantics.get("base_models", []) if model else [])
    return any(cls in allowed for cls in lineage)


def _cardinality_errors(edges: list[EdgeRecord], relation_types: dict[str, dict[str, Any]]) -> list[str]:
    out_count = Counter((e.source, e.relation) for e in edges)
    in_count = Counter((e.target, e.relation) for e in edges)
    errors = [f"{src} has {n} '{rel}' targets but cardinality is {_card(relation_types, rel)}" for (src, rel), n in out_count.items() if n > 1 and _card(relation_types, rel) in ("one_to_one", "many_to_one")]
    return errors + [f"{tgt} has {n} '{rel}' sources but cardinality is {_card(relation_types, rel)}" for (tgt, rel), n in in_count.items() if n > 1 and _card(relation_types, rel) in ("one_to_one", "one_to_many")]


def _card(relation_types: dict[str, dict[str, Any]], relation: str) -> str:
    return relation_types.get(relation, {}).get("cardinality", "many_to_many")
