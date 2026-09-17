"""Every derived index of a store, in the order they depend on each other: a document's tags
(semantic), then its sections (they carry the tags), then its edges (they carry both)."""

from __future__ import annotations

from pathlib import Path

from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import RebuildReport, rebuild_semantic_indexes


def rebuild_derived_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None) -> RebuildReport:
    """Semantic, sections and edges indexes brought current; used where a model (not one
    document) changed — registered, reindexed, promoted — so its node, fields and every
    document hash that moved reach the edge index in the same operation.

    Returns:
        The semantic rebuild's report (what those callers already reported).
    """
    report = rebuild_semantic_indexes(store_path, project_root, resolve_model_ref, pythonpath)
    rebuild_sections_indexes(store_path, project_root, resolve_model_ref, pythonpath)
    rebuild_edges_indexes(store_path, project_root, resolve_model_ref, pythonpath)
    return report
