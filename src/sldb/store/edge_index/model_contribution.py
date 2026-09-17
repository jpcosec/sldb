"""What a registered model contributes: its node, a node per field, `has_field`, `extends`."""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import field_node_id, model_node_id
from sldb.store.edge_index.records import edge, tag_nodes, tagged_as
from sldb.store.models import EdgeNodeRecord, ModelEdges, ModelsIndex


def build_model_edges(m_idx: ModelsIndex, model_type: Any | None) -> ModelEdges:
    """The model's shard. `hash_b` is left out of the node on purpose: it moves with every
    document write, and the documents' own shards already carry their hashes.

    Args:
        m_idx: The model's index record (ref, path, version, semantics, base models).
        model_type: The imported model class, or None when it cannot be imported here (a
            linked store's model): the node is still contributed, its fields are not.

    Returns:
        The shard, not yet stamped with `edges_version`.
    """
    mid = model_node_id(m_idx.name)
    tags = sorted(set(m_idx.semantics))
    nodes = [_model_node(m_idx, mid, tags)] + tag_nodes(tags)
    edges = tagged_as(mid, tags)
    if model_type is not None:
        nodes += [_field_node(m_idx.name, fname, finfo) for fname, finfo in model_type.model_fields.items()]
        edges += [edge(mid, field_node_id(m_idx.name, fname), "has_field", "schema") for fname in model_type.model_fields]
        edges += [edge(mid, model_node_id(base), "extends", "schema") for base in sorted(set(m_idx.base_models))]
    return ModelEdges(model_name=m_idx.name, nodes=nodes, edges=edges)


def _model_node(m_idx: ModelsIndex, mid: str, tags: list[str]) -> EdgeNodeRecord:
    semantics = {"name": m_idx.name, "model_ref": m_idx.model_ref, "path": m_idx.path, "version": m_idx.version, "canonical": m_idx.canonical, "family": m_idx.family, "semantic_tags": tags, "base_models": sorted(set(m_idx.base_models))}
    return EdgeNodeRecord(id=mid, node_type="sldb_model", semantics=semantics)


def _field_node(model_name: str, fname: str, finfo: Any) -> EdgeNodeRecord:
    from sldb.api.schema.describe_field import describe_field  # a pydantic-only leaf; imported late so sldb.store never loads sldb.api at import time

    desc = describe_field(fname, finfo).model_dump(exclude={"annotation", "description"}, exclude_none=True)
    desc.update({"model": model_name, "description": finfo.description or ""})
    return EdgeNodeRecord(id=field_node_id(model_name, fname), node_type="sldb_field", semantics=desc)
