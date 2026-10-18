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

    found = []
    for doc in load_runtime_documents(store_path, resolve_model_ref, pythonpath):
        path = project_root / doc.path
        if doc.model_type is not None and path.exists() and (lost := rewrite_loss(doc.model_type, path.read_text(encoding="utf-8"))):
            found.append({"document": doc.name, "model": doc.model_name, "path": doc.path, "lost": lost})
    return found
