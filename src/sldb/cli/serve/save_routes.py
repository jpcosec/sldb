"""POST /save: single-document write (legacy) and batched optimistic writes.

The batch prevalidates every change before writing anything, applies in
create→update→delete order under a module lock, and reports partial failure
with the ids already completed so clients retry only the outstanding ones.
All store logic comes from ``sldb.api`` — nothing is reimplemented here.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from sldb.api.documents.create_document import create_document
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.untrack_document import untrack_document
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.save_plan import bad, prevalidate
from sldb.cli.serve.save_single import save_single
from sldb.store.query import load_runtime_documents

SAVE_LOCK = threading.RLock()
_CHANGE_LIMIT = 500
_ACTION_ORDER = {"create": 0, "update": 1, "delete": 2}


def save_request(request: dict[str, Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    with SAVE_LOCK:
        if "changes" in request:
            return batch_save(request, store_path, project_root, pythonpath)
        return save_single(request, store_path, pythonpath)


def batch_save(request: dict[str, Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    if not batch_shape(request):
        return bad("Lista de cambios inválida.")
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    current = {doc.name: doc for doc in docs}
    prepared, error = prepare_batch(request["changes"], current, docs, store_path, project_root, pythonpath)
    if error is not None:
        return error
    return apply_batch(prepared, store_path, pythonpath)


def batch_shape(request: dict[str, Any]) -> bool:
    changes = request.get("changes")
    return isinstance(changes, list) and len(changes) <= _CHANGE_LIMIT


def prepare_batch(changes: list[Any], current: dict[str, Any], docs: list[Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[list[tuple[dict[str, Any], Any, Path | None]], tuple[dict[str, Any], int] | None]:
    seen, prepared = set(), []
    for change in changes:
        step, error = prepare_step(change, seen, current, docs, store_path, project_root, pythonpath)
        if error is not None:
            return [], error
        prepared.append(step)
    return prepared, None


def prepare_step(change: Any, seen: set[str], current: dict[str, Any], docs: list[Any], store_path: Path, project_root: Path, pythonpath: str) -> tuple[tuple[dict[str, Any], Any, Path | None] | None, tuple[dict[str, Any], int] | None]:
    name, error = change_name(change, seen)
    if error is not None:
        return None, error
    seen.add(name)
    path, error = prevalidate(change, name, current, docs, store_path, project_root, pythonpath)
    if error is not None:
        return None, error
    return (change, current.get(name), path), None


def change_name(change: Any, seen: set[str]) -> tuple[str | None, tuple[dict[str, Any], int] | None]:
    name = change.get("id") if isinstance(change, dict) else None
    if not isinstance(name, str) or name in seen:
        return None, bad("Identificador duplicado o inválido.")
    return name, None


def apply_batch(prepared: list[tuple[dict[str, Any], Any, Path | None]], store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    completed: list[str] = []
    try:
        for change, current, path in sorted(prepared, key=sort_key):
            apply_change(change, current, path, store_path, pythonpath)
            completed.append(change["id"])
    except (Exception, SystemExit) as exc:
        return {"ok": False, "error": f"No se completó el guardado: {exc}", "completed": completed}, 500
    return {"ok": True, "saved": completed}, 200


def sort_key(item: tuple[dict[str, Any], Any, Path | None]) -> int:
    return _ACTION_ORDER[item[0]["action"]]


def apply_change(change: dict[str, Any], current: Any, path: Path | None, store_path: Path, pythonpath: str) -> None:
    name, action = change["id"], change["action"]
    if action == "create":
        create_document(store_path, change["model"], path, change["payload"], name=name, pythonpath=pythonpath)
    elif action == "update":
        save_document_payload(store_path, current.model_name, name, change["payload"], pythonpath=pythonpath)
    else:
        untrack_document(store_path, name, pythonpath=pythonpath)