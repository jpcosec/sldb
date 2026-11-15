"""Which nodes of the graph enter the component spec: type, model and module scope (from `spec2viz.graph_import`)."""

from __future__ import annotations

from sldb.api.notations.component_spec_constants import GraphAttrs
from sldb.api.notations.component_spec_ids import document_ref, node_kind


def _keeps(node_id: str, node_type: str, wanted_types: tuple, wanted_models: tuple) -> bool:
    """1. El nodo pasa los filtros de tipo y de modelo."""
    kind = node_kind(node_id, node_type)
    if kind not in wanted_types:
        return False
    if wanted_models and kind == "document":
        return document_ref(node_id, node_type)[0] in wanted_models
    return True


def _in_scope(node_id: str, attrs: GraphAttrs, prefixes: tuple) -> bool:
    if not prefixes:
        return True
    module = attrs.get(node_id, {}).get("module") or (node_id[len("python:"):] if node_id.startswith("python:") else node_id)
    return any(module == p or module.startswith(p + ".") for p in prefixes)
