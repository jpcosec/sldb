"""`sldb_kgdb_semantic_export` v1 -> GraphSnapshot, the kgdb `ingest/sldb.py` route."""

from __future__ import annotations

from typing import Any

from sldb.store.graph.ingest_sldb_nodes import (
    _document_node,
    _model_node,
    _section_node,
    _semantic_tag_node,
    _store_node,
)
from sldb.store.graph.snapshot import GraphSnapshot

CONTRACT_NAME = "sldb_kgdb_semantic_export"
CONTRACT_VERSION = 1


def sldb_semantic_export_to_snapshot(payload: dict[str, Any]) -> GraphSnapshot:
    """Convert an SLDB semantic export payload into a KGDB graph snapshot."""
    _validate_contract(payload)
    provenance = _base_provenance(payload)
    tag_ids = _collect_semantic_tags(payload)
    return GraphSnapshot(version="1.0", nodes=_build_nodes(payload, provenance, tag_ids), metadata=_metadata(payload))


def _validate_contract(payload: dict[str, Any]) -> None:
    contract = payload.get("contract", {})
    if contract.get("name") != CONTRACT_NAME or contract.get("version") != CONTRACT_VERSION:
        raise ValueError(f"Expected {CONTRACT_NAME} version {CONTRACT_VERSION}")


def _base_provenance(payload: dict[str, Any]) -> dict[str, Any]:
    return {"contract": payload["contract"], "producer": payload["producer"], "store": _store_provenance(payload["store"])}


def _store_provenance(store: dict[str, Any]) -> dict[str, Any]:
    return {"root": store["root"], "store_path": store["store_path"], "hash_a": store["hash_a"], "runtime_sources": store.get("runtime_sources", {})}


def _collect_semantic_tags(payload: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for model in payload["models"]:
        tags.update(model["semantics"])
    for document in payload["documents"]:
        tags.update(document["semantic_tags"])
    for section in payload["sections"]:
        tags.update(section["semantic_tags"])
    return tags | _dag_tags(payload["semantic_dag"])


def _dag_tags(dag: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for node in dag["nodes"]:
        tags.add(node["id"])
        tags.update(node["parents"])
    for tag, equivalents in dag["equivalences"].items():
        tags.add(tag)
        tags.update(equivalents)
    return tags


def _build_nodes(payload: dict[str, Any], provenance: dict[str, Any], tag_ids: set[str]) -> list:
    store_node_id = "sldb://store"
    nodes = [_store_node(payload, store_node_id, provenance)]
    nodes += [_semantic_tag_node(tag, payload, provenance) for tag in sorted(tag_ids)]
    nodes += [_model_node(m, _documents_of(payload, m), store_node_id, provenance) for m in payload["models"]]
    nodes += [_document_node(d, _sections_of(payload, d), provenance) for d in payload["documents"]]
    nodes += [_section_node(s, provenance) for s in payload["sections"]]
    return nodes


def _documents_of(payload: dict[str, Any], model: dict[str, Any]) -> list:
    return [d for d in payload["documents"] if d["model"] == model["name"]]


def _sections_of(payload: dict[str, Any], document: dict[str, Any]) -> list:
    return [s for s in payload["sections"] if s["document_id"] == document["id"]]


def _metadata(payload: dict[str, Any]) -> dict[str, Any]:
    return {"source_contract": payload["contract"], "producer": payload["producer"], "store": payload["store"], "generated_from": CONTRACT_NAME}
