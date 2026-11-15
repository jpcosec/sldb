"""Models and relation types of the store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import document_address, model_address, relation_type_address
from sldb.mcp.paging import page
from sldb.mcp.read.miss import missing


def model_item(entry: Any) -> dict[str, Any]:
    """One registered model, with its stable address."""
    return {"address": model_address(entry.name), "name": entry.name, "model_ref": entry.model_ref, "origin": entry.origin, "version": entry.version, "family": entry.family, "semantics": list(entry.semantics)}


def list_models(store_path: Path, offset: int, limit: int) -> dict[str, Any]:
    """Every model the store registers (its own and the inherited ones)."""
    items = [model_item(entry) for entry in api.registered_models(store_path)]
    return page(items, offset, limit, None if items else "the store registers no model")


def describe_model(store_path: Path, model: str, offset: int, limit: int) -> dict[str, Any]:
    """A model's contract (fields with their types) and a page of its tracked documents."""
    if not api.is_model_registered(store_path, model):
        return missing("unknown_model", model, {"found": False, "model": model, "explanation": f"the store does not register a model named {model!r}; list_models names the ones it does"})
    description = api.describe_model(store_path, model).model_dump(mode="json")
    documents = [{"address": document_address(f"{description['name']}:{d['name']}"), **d} for d in description.pop("documents")]
    shown = page(documents, offset, limit, None if documents else f"the store tracks no document of {model}")
    return {"found": True, "address": model_address(description["name"]), **description, "documents": shown}


def list_relation_types(store_path: Path, offset: int, limit: int) -> dict[str, Any]:
    """The relation types of the edge index (this store's and its linked stores')."""
    nodes = api.edge_nodes_of_type(store_path, "relation_type")
    items = [{"address": n.id, "name": api.bare(n.id), **n.semantics} for n in nodes]
    return page(items, offset, limit, None if items else "the edge index declares no relation type")


def describe_relation_type(store_path: Path, name: str) -> dict[str, Any]:
    """One relation type: its endpoints, direction, cardinality and description."""
    node = api.edge_node(store_path, relation_type_address(name))
    if node is None:
        return missing("unknown_relation", name, {"found": False, "name": name, "explanation": f"the edge index declares no relation type {name!r}; list_relation_types names the ones it does"})
    return {"found": True, "address": node.id, "name": api.bare(node.id), **node.semantics}
