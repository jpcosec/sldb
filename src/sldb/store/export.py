from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Callable

from sldb.store.io import (
    load_documents_index, load_models_index, load_sections_index,
    load_semantic_dag, load_store_index, store_lock,
)
from sldb.store.layout import semantic_dag_path, semantic_index_path, store_index_path
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


class SemanticExporter:
    """Exports the KGDB semantic payload from persisted SLDB indexes."""

    def __init__(self, store_path: Path, project_root: Path):
        self.store_path = store_path
        self.project_root = project_root

    def export(self, resolve_ref: Callable[..., Any] | None = None, pythonpath: str | None = None, *, rebuild: bool = False, command: list[str] | None = None) -> dict[str, Any]:
        """Build the export payload."""
        if rebuild:
            self._rebuild(resolve_ref, pythonpath)
        return self._build_payload(command)

    def _rebuild(self, resolve_ref, pythonpath):
        if resolve_ref is None:
            raise ValueError("resolve_model_ref is required")
        with store_lock(self.store_path):
            rebuild_semantic_indexes(self.store_path, self.project_root, resolve_ref, pythonpath)
            rebuild_sections_indexes(self.store_path, self.project_root, resolve_ref, pythonpath)
            rebuild_edges_indexes(self.store_path, self.project_root, resolve_ref, pythonpath)

    def _build_payload(self, command) -> dict[str, Any]:
        st_idx = load_store_index(self.store_path)
        dag = load_semantic_dag(self.store_path)
        mods, docs, secs = self._proc_models(st_idx)
        return {"contract": {"name": "sldb_kgdb_semantic_export", "version": 1, "generated_at": _utc_now()}, "producer": {"name": "sldb", "version": _version(), "command": command or []}, "store": self._store_meta(st_idx, mods), "models": mods, "documents": docs, "sections": secs, "semantic_dag": self._dag_meta(dag)}

    def _proc_models(self, st_idx):
        mods, docs, secs = [], [], []
        for m_entry in sorted(st_idx.models, key=lambda i: i.name):
            self._proc_entry(m_entry, mods, docs, secs)
        return mods, docs, secs

    def _proc_entry(self, m_entry, mods, docs, secs):
        m_idx = load_models_index(self.project_root / m_entry.models_index)
        d_idx = load_documents_index(self.project_root / m_idx.documents_index)
        s_idx = load_sections_index(self.project_root / m_idx.sections_index) if m_idx.sections_index else None
        mods.append({"name": m_idx.name, "model_ref": m_idx.model_ref, "path": m_idx.path, "models_index": m_entry.models_index, "documents_index": m_idx.documents_index, "sections_index": m_idx.sections_index, "version": m_idx.version, "canonical": m_idx.canonical, "family": m_idx.family, "semantics": sorted(set(m_idx.semantics)), "base_models": sorted(set(m_idx.base_models)), "hash_b": m_idx.hash_b})
        self._proc_docs(d_idx, m_idx, docs)
        if s_idx:
            self._proc_secs(s_idx, m_idx, secs)

    def _proc_docs(self, d_idx, m_idx, docs):
        for d in sorted(d_idx.documents, key=lambda i: i.name):
            docs.append({"id": f"{m_idx.name}:{d.name}", "name": d.name, "model": m_idx.name, "path": d.path, "hash_c": d.hash_c, "hash_d": d.hash_d, "semantic_tags": sorted(set(d.semantic_tags))})

    def _proc_secs(self, s_idx, m_idx, secs):
        for d_s in sorted(s_idx.documents, key=lambda i: i.doc_name):
            d_id = f"{m_idx.name}:{d_s.doc_name}"
            for s in d_s.sections:
                secs.append({"id": f"{d_id}#{s.path}", "document_id": d_id, "path": s.path, "title": s.title, "breadcrumbs": s.breadcrumbs, "about": s.about, "semantic_tags": s.semantic_tags, "slug": s.slug, "level": s.level, "line_start": s.line_start, "line_end": s.line_end})

    def _store_meta(self, st_idx, mods):
        return {"root": str(self.project_root), "store_path": str(self.store_path), "hash_a": st_idx.hash_a, "runtime_sources": {"store_index": _disp(store_index_path(self.store_path), self.project_root), "semantic_index": _disp(semantic_index_path(self.store_path), self.project_root), "semantic_dag": _disp(semantic_dag_path(self.store_path), self.project_root), "sections_indexes": [m["sections_index"] for m in mods if m.get("sections_index")]}}

    def _dag_meta(self, dag):
        return {"nodes": [{"id": n.id, "parents": sorted(set(n.parents))} for n in sorted(dag.nodes, key=lambda i: i.id)], "equivalences": {k: sorted(set(v)) for k, v in sorted(dag.equivalences.items())}}

def export_kgdb_semantic_payload(store_path: Path, project_root: Path, resolve_model_ref: Callable[..., Any] | None = None, pythonpath: str | None = None, *, rebuild: bool = False, command: list[str] | None = None) -> dict[str, Any]:
    """Build the KGDB semantic export payload from persisted SLDB indexes."""
    return SemanticExporter(store_path, project_root).export(resolve_model_ref, pythonpath, rebuild=rebuild, command=command)

def _disp(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)

def _version() -> str:
    try:
        return version("sldb")
    except PackageNotFoundError:
        return "0.1.0"

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
