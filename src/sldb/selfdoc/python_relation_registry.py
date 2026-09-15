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
    registry = {
        str(doc.payload["name"]): doc.payload
        for doc in documents
        if doc.model_name == "RelationTypeDoc" and doc.payload.get("name") in RELATIONS
    }
    missing = sorted(RELATIONS - registry.keys())
    if missing:
        raise ValueError(
            "Python source relations are not registered in KGDB: "
            + ", ".join(missing)
        )
    return registry


def validate_source_snapshot(snapshot: dict, registry: dict[str, dict]) -> None:
    """Require every AST edge to use its registered endpoint and cardinality rules."""
    nodes = {
        node["identity"]["node_id"]: node["identity"]["node_type"]
        for node in snapshot["nodes"]
    }
    errors: list[str] = []
    outbound: Counter[tuple[str, str]] = Counter()
    inbound: Counter[tuple[str, str]] = Counter()
    for node in snapshot["nodes"]:
        source, source_type = node["identity"]["node_id"], node["identity"]["node_type"]
        for edge in node["edges"]:
            relation, target = edge["relation_type"], edge["target_id"]
            if relation not in RELATIONS:
                continue
            spec = registry.get(relation)
            where = f"{source} -[{relation}]-> {target}"
            if spec is None:
                errors.append(f"{where}: relation type is not registered")
                continue
            target_type = nodes.get(target)
            if target_type is None:
                errors.append(f"{where}: target does not exist")
                continue
            if source_type not in spec["source_types"]:
                errors.append(f"{where}: source type {source_type!r} is not allowed")
            if target_type not in spec["target_types"]:
                errors.append(f"{where}: target type {target_type!r} is not allowed")
            outbound[source, relation] += 1
            inbound[target, relation] += 1
    _validate_cardinality(registry, outbound, inbound, errors)
    if errors:
        raise ValueError("Invalid Python source graph:\n- " + "\n- ".join(errors))


def _validate_cardinality(registry, outbound, inbound, errors) -> None:
    for (node, relation), count in outbound.items():
        if count > 1 and registry[relation]["cardinality"] in ("one_to_one", "many_to_one"):
            errors.append(f"{node} has {count} {relation!r} targets")
    for (node, relation), count in inbound.items():
        if count > 1 and registry[relation]["cardinality"] in ("one_to_one", "one_to_many"):
            errors.append(f"{node} has {count} {relation!r} sources")
