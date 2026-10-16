"""Every edge checked against its relation type (kgdb's TypedIngestError, as a report): the
type is a tracked RelationTypeDoc, the target exists, both endpoint classes are allowed (model
names inherit through `base_models`), and cardinality holds.

In a store that ran `edges init`, an edge sldb derives itself (structural, schema, alias)
whose builtin type the store has not tracked is checked against the definition sldb ships: a
builtin added after that init must not fail every existing store. A store that never ran
`edges init` still fails, as before. `untracked_builtins` names those types so
the gap is reported, not hidden; authored edges still need a tracked type."""

from __future__ import annotations

from collections import Counter
from typing import Any

from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.resolve import relation_types_of
from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_payload
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_BUILTIN_ORIGINS = ("structural", "schema", "alias")
_SHIPPED = {spec["name"]: builtin_payload(spec) for spec in BUILTIN_RELATION_TYPES}


def validate_edge_index(index: EdgeIndex) -> list[str]:
    """The violations found, as sentences; empty when every edge is valid."""
    tracked = relation_types_of(index.nodes)
    effective = _effective_types(tracked)
    errors: list[str] = []
    for e in index.edges:
        errors += _edge_errors(index.nodes, e, (effective if _derived(e) else tracked).get(e.relation))
    return errors + _cardinality_errors(index.edges, effective)


def untracked_builtins(index: EdgeIndex) -> list[str]:
    """Builtin types newer than the store's `edges init` that its derived edges use (re-run init to track them)."""
    tracked = relation_types_of(index.nodes)
    if not _initialised(tracked):
        return []
    return sorted({e.relation for e in index.edges if e.relation not in tracked and e.relation in _SHIPPED and _derived(e)})


def _effective_types(tracked: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """The tracked types, completed with the shipped builtins once the store ran `edges init`."""
    return {**_SHIPPED, **tracked} if _initialised(tracked) else tracked


def _initialised(tracked: dict[str, dict[str, Any]]) -> bool:
    return any(name in _SHIPPED for name in tracked)


def _derived(e: EdgeRecord) -> bool:
    return e.metadata.get("origin") in _BUILTIN_ORIGINS


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
