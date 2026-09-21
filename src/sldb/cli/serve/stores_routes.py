"""GET /stores and GET /stores/check.

`/stores` describes the store this server serves: root, model/document counts,
hash_a and the linked stores — the view `sldb stores list` prints. `/stores/check`
runs the CLI's real integrity verification (`sldb.api.check_store` →
``diagnose_store``) and reports every document whose shard hash no longer matches
its recorded hash_c/hash_d.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import check_store
from sldb.core.exceptions import SLDBError
from sldb.store.io import load_documents_index, load_models_index, load_store_index


def dispatch_stores(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    if route == "/stores/check":
        return _check(store_path, project_root, pythonpath)
    return _describe(store_path, project_root), 200


def _describe(store_path: Path, root: Path) -> dict[str, Any]:
    index = load_store_index(store_path)
    return {
        "store": str(store_path),
        "root": str(root),
        "model_count": len(index.models),
        "doc_count": _doc_count(store_path, root, index),
        "hash_a": index.hash_a,
        "stores": [{"name": entry.name, "path": entry.path} for entry in sorted(index.stores, key=lambda s: s.name)],
    }


def _doc_count(store_path: Path, root: Path, index: Any) -> int:
    total = 0
    for model in index.models:
        models_index = load_models_index(root / model.models_index)
        total += len(load_documents_index(root / models_index.documents_index).documents)
    return total


def _check(store_path: Path, root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    try:
        return check_store(store_path, root, pythonpath), 200
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 400