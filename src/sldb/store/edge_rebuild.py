"""The edge index brought current (mirror of section_rebuild; the port of kgdb's typed
ingest lives in `sldb.store.edge_index`): the store's shard, then every model's and every
document's. Runs after the semantic and sections rebuilds — a document's shard is built from
its index entry's tags and its sections shard."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from sldb.core.exceptions import SLDBModelError
from sldb.store.codec import default_codec
from sldb.store.edge_index.cache_keys import edge_shard_version
from sldb.store.edge_index.doc_contribution import build_doc_edges
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.shard_signature import note_rebuild
from sldb.store.edge_index.store_contribution import build_store_edges
from sldb.store.edge_sync import process_model_edges
from sldb.store.io import load_semantic_dag, load_store_index
from sldb.store.io.shards import delete_shard, load_sections_shard, save_edges_shard
from sldb.store.layout import edges_shards_root, edges_store_shard_path, sections_shard_path

logger = logging.getLogger(__name__)


def rebuild_edges_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None, report: EdgeRebuildReport | None = None, full: bool = False) -> EdgeRebuildReport:
    """Every shard of the store's edge index, current; only what moved is rewritten. `full`
    compares every document's shard instead of trusting the per-model cache and dirty set."""
    report = report or EdgeRebuildReport()
    st_idx = load_store_index(store_path)
    _save_store_shard(store_path, st_idx)
    for m in st_idx.models:
        resolve = lambda m=m: _model_type(resolve_model_ref, m, pythonpath, project_root, report)  # noqa: E731
        process_model_edges(m, project_root, report, store_path, resolve, lambda m_entry, m_type, doc: _doc_edges(store_path, project_root, m_entry, m_type, doc), full)
    _prune_models(store_path, {m.name for m in st_idx.models})
    if report.models_walked:
        note_rebuild(store_path)
    return report


def _save_store_shard(store_path: Path, st_idx) -> None:
    shard = build_store_edges(st_idx, load_semantic_dag(store_path)).model_copy(update={"edges_version": edge_shard_version()})
    save_edges_shard(edges_store_shard_path(store_path), shard)


def _model_type(resolver, m_entry, pythonpath: str | None, root: Path, report: EdgeRebuildReport) -> Any | None:
    """The model class, tried from the caller's path and then the store's own root (a linked
    store's models import from there); None, and reported, when neither works."""
    for candidate in (pythonpath, str(root)):
        try:
            return resolver(m_entry.model_ref, candidate)
        except SLDBModelError as exc:
            logger.debug("edges: %s not importable from %s: %s", m_entry.model_ref, candidate, exc)
    report.models_unresolved.append(m_entry.name)
    return None


def _doc_edges(store_path: Path, root: Path, m_entry, model_type: Any | None, doc):
    sections = load_sections_shard(sections_shard_path(store_path, m_entry.name, doc.name))
    read_payload = lambda: None if model_type is None else default_codec.extract(model_type, (root / doc.path).read_text(encoding="utf-8"))  # noqa: E731
    return build_doc_edges(m_entry.name, doc, sections.sections if sections else [], read_payload)


def _prune_models(store_path: Path, registered: set[str]) -> None:
    """Shards of a model that is no longer registered go with it: its file and its directory."""
    root = edges_shards_root(store_path)
    for path in sorted(root.iterdir()) if root.is_dir() else []:
        if (path.stem if path.is_file() else path.name) in registered:
            continue
        for shard in [path] if path.is_file() else sorted(path.glob("*.yaml")):
            delete_shard(shard)
        if path.is_dir():
            path.rmdir()
