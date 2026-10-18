"""Every edge checked against its relation type, as a report rather than an exception: the
type is a tracked RelationTypeDoc, the target exists, both endpoint classes are allowed (model
names inherit through `base_models`), and cardinality holds.

In a store that ran `edges init`, an edge sldb derives itself (structural, schema, alias)
whose builtin type the store has not tracked is checked against the definition sldb ships: a
builtin added after that init must not fail every existing store, and a type authored under a
builtin's name does not retype the edges sldb derives. A store that never ran
`edges init` still fails, as before. `untracked_builtins` names those types so
the gap is reported, not hidden; authored edges still need a tracked type."""

from __future__ import annotations

from collections import Counter
from typing import Any

from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.resolve import relation_types_of
from sldb.store.model_contract import BUILTIN_RELATION_TYPES, builtin_payload
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_BUILTIN_ORIGINS = ("structural", "schema", "alias")
_SHIPPED = {spec["name"]: builtin_payload(spec) for spec in BUILTIN_RELATION_TYPES}


def validate_edge_index(index: EdgeIndex) -> list[str]:
    """The violations found, as sentences; empty when every edge is valid."""
    own, linked = validate_edge_index_by_store(index)
    return own + linked


def validate_edge_index_by_store(index: EdgeIndex) -> tuple[list[str], list[str]]:
    """(violations of this store's own edges, those only a linked store's edges commit).

    A cardinality violation is this store's when any edge behind it is; an edge a linked store
    contributes that this store also contributes (a shared model's fields) is this store's."""
    tracked = relation_types_of(index.nodes)
    effective = _effective_types(tracked)
    own_keys = {_key(e) for e in index.edges if "from_store" not in e.metadata}
    own: list[str] = []
    linked: list[str] = []
    for e in index.edges:
        (linked if _key(e) not in own_keys else own).extend(_edge_errors(index.nodes, e, (effective if _derived(e) else tracked).get(e.relation)))
    cardinality = _cardinality_errors([e for e in index.edges if _derived(e)], effective, own_keys) + _cardinality_errors([e for e in index.edges if not _derived(e)], {**_SHIPPED, **tracked}, own_keys)
    return list(dict.fromkeys(own + [m for m, mine in cardinality if mine])), list(dict.fromkeys(m for m in linked + [m for m, mine in cardinality if not mine] if m not in own))


def _key(e: EdgeRecord) -> tuple[str, str, str]:
    return (e.source, e.relation, e.target)


def untracked_builtins(index: EdgeIndex) -> list[str]:
    """Builtin types newer than the store's `edges init` that its derived edges use (re-run init to track them)."""
    tracked = relation_types_of(index.nodes)
    if not _initialised(tracked):
        return []
    return sorted({e.relation for e in index.edges if e.relation not in tracked and e.relation in _SHIPPED and _derived(e)})


def _effective_types(tracked: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """The types a derived edge is checked against once the store ran `edges init`: sldb's own
    definition of a builtin wins, since sldb produces those edges. A store may author a type
    under a builtin's name (selfdoc's code `contains`); it applies to authored edges only."""
    return {**tracked, **_SHIPPED} if _initialised(tracked) else tracked


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


def _cardinality_errors(edges: list[EdgeRecord], relation_types: dict[str, dict[str, Any]], own_keys: set) -> list[tuple[str, bool]]:
    """(violation, whether an edge of this store is behind it)."""
    unique = {_key(e) for e in edges}  # one fact two stores both emit (a shared model's fields) is one edge
    out_count = Counter((src, rel) for src, rel, _ in unique)
    in_count = Counter((tgt, rel) for _, rel, tgt in unique)
    out_own = {(s_, r) for s_, r, t in unique if (s_, r, t) in own_keys}
    in_own = {(t, r) for s_, r, t in unique if (s_, r, t) in own_keys}
    errors = [(f"{src} has {n} '{rel}' targets but cardinality is {_card(relation_types, rel)}", (src, rel) in out_own) for (src, rel), n in out_count.items() if n > 1 and _card(relation_types, rel) in ("one_to_one", "many_to_one")]
    return errors + [(f"{tgt} has {n} '{rel}' sources but cardinality is {_card(relation_types, rel)}", (tgt, rel) in in_own) for (tgt, rel), n in in_count.items() if n > 1 and _card(relation_types, rel) in ("one_to_one", "one_to_many")]


def _card(relation_types: dict[str, dict[str, Any]], relation: str) -> str:
    return relation_types.get(relation, {}).get("cardinality", "many_to_many")
