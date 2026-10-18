"""Every tracked document a rewrite would lose content from, with what it would lose.

Diagnosis, beside the structural noise scan: the hashes of a document its model cannot read
stay consistent over the empty extraction, so nothing else delates it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def scan_rewrite_loss(store_path: Path, project_root: Path, pythonpath: str | None = None) -> list[dict[str, Any]]:
    """One `{document, model, path, lost}` per document whose rewrite would drop blocks."""
    from sldb.api.documents.rewrite_loss import rewrite_loss
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    from sldb.api.stores.scan_cache import cached_per_document

    docs = [(d, (project_root / d.path).read_text(encoding="utf-8")) for d in load_runtime_documents(store_path, resolve_model_ref, pythonpath) if d.model_type is not None and (project_root / d.path).exists()]
    scanned = cached_per_document(store_path, "rewrite-loss", docs, lambda doc, text: rewrite_loss(doc.model_type, text, doc.payload))
    return [{"document": d.name, "model": d.model_name, "path": d.path, "lost": lost} for d, lost in scanned if lost]
