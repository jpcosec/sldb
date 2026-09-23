"""Validate AST-derived edges against the store's KGDB relation vocabulary."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query import load_runtime_documents

RELATIONS = frozenset({"contains", "imports", "references"})


def registered_source_relations(store: Path, root: Path) -> dict[str, dict]:
    """Load the registered KGDB relation types, never a private adapter copy."""
    documents = load_runtime_documents(store, resolve_model_ref, str(root))
    registry = _relation_registry(documents)
    _require_registered(registry)
    return registry


def _relation_registry(documents) -> dict[str, dict]:
    return {
        str(doc.payload["name"]): doc.payload
        for doc in documents
        if doc.model_name == "RelationTypeDoc" and doc.payload.get("name") in RELATIONS
    }


def _require_registered(registry) -> None:
    missing = sorted(RELATIONS - registry.keys())
    if missing:
        raise ValueError(
            "Python source relations are not registered in KGDB: "
            + ", ".join(missing)
        )


def validate_source_snapshot(snapshot: dict, registry: dict[str, dict]) -> None:
    """Require every AST edge to use its registered endpoint and cardinality rules."""
    nodes = _node_types(snapshot)
    errors: list[str] = []
    outbound: Counter[tuple[str, str]] = Counter()
    inbound: Counter[tuple[str, str]] = Counter()
    for node in snapshot["nodes"]:
        _validate_node(node, nodes, registry, errors, outbound, inbound)
    _validate_cardinality(registry, outbound, inbound, errors)
    if errors:
        raise ValueError("Invalid Python source graph:\n- " + "\n- ".join(errors))


def _node_types(snapshot) -> dict[str, str]:
    return {
        node["identity"]["node_id"]: node["identity"]["node_type"]
        for node in snapshot["nodes"]
    }


def _validate_node(node, nodes, registry, errors, outbound, inbound) -> None:
    source, source_type = node["identity"]["node_id"], node["identity"]["node_type"]
    for edge in node["edges"]:
        _validate_edge(edge, source, source_type, nodes, registry, errors, outbound, inbound)


def _validate_edge(edge, source, source_type, nodes, registry, errors, outbound, inbound) -> None:
    relation, target = edge["relation_type"], edge["target_id"]
    if relation not in RELATIONS or not _can_track(relation, target, source, nodes, registry, errors):
        return
    _check_types(source, relation, target, source_type, nodes[target], registry[relation], errors)
    outbound[source, relation] += 1; inbound[target, relation] += 1


def _can_track(relation, target, source, nodes, registry, errors) -> bool:
    where = f"{source} -[{relation}]-> {target}"
    if registry.get(relation) is None:
        errors.append(f"{where}: relation type is not registered")
        return False
    if nodes.get(target) is None:
        errors.append(f"{where}: target does not exist")
        return False
    return True


def _check_types(source, relation, target, source_type, target_type, spec, errors) -> None:
    where = f"{source} -[{relation}]-> {target}"
    if source_type not in spec["source_types"]:
        errors.append(f"{where}: source type {source_type!r} is not allowed")
    if target_type not in spec["target_types"]:
        errors.append(f"{where}: target type {target_type!r} is not allowed")


def _validate_cardinality(registry, outbound, inbound, errors) -> None:
    for (node, relation), count in outbound.items():
        if count > 1 and registry[relation]["cardinality"] in ("one_to_one", "many_to_one"):
            errors.append(f"{node} has {count} {relation!r} targets")
    for (node, relation), count in inbound.items():
        if count > 1 and registry[relation]["cardinality"] in ("one_to_one", "one_to_many"):
            errors.append(f"{node} has {count} {relation!r} sources")