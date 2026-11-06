"""POST /save: single-document write (legacy) and batched optimistic writes.

The batch is checked here for its HTTP contract (shape, ids, stale `expected`, targets) and
handed whole to ``sldb.api.apply_batch``, which prevalidates it against the models and writes
it in one transaction: a failure halfway rolls every change back (``rolled_back: true``);
nothing is saved partially any more. Nothing of the store is reimplemented here.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from sldb.api.documents.apply_batch import apply_batch
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.save_plan import bad, prevalidate
from sldb.cli.serve.save_single import save_single
from sldb.core.exceptions import ConflictError, SLDBStoreError, SLDBValidationError
from sldb.store.query import load_runtime_documents

SAVE_LOCK = threading.RLock()
_CHANGE_LIMIT = 500


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
    return apply_prepared(prepared, store_path, pythonpath)


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


def apply_prepared(prepared: list[tuple[dict[str, Any], Any, Path | None]], store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """The whole batch through `apply_batch`: its prevalidation errors keep their HTTP status
    (409 conflict or taken target, 422 payload); a failure while applying is a 500 that rolled
    everything back."""
    try:
        report = apply_batch(store_path, [with_target(change, path) for change, _current, path in prepared], pythonpath)
    except ConflictError as exc:
        return bad(f"{exc.ref} cambió en SLDB. Recarga para evitar sobrescribirlo.", 409)
    except (SLDBStoreError, SLDBValidationError) as exc:
        return bad(str(exc), 422 if isinstance(exc, SLDBValidationError) else 409)
    except (Exception, SystemExit) as exc:
        return {"ok": False, "error": f"No se completó el guardado: {exc}", "rolled_back": True}, 500
    return {"ok": True, "saved": report.saved}, 200


def with_target(change: dict[str, Any], path: Path | None) -> dict[str, Any]:
    """A create carries the path prevalidation chose for it, so /save keeps placing new files
    beside the model's existing documents."""
    return {**change, "path": str(path)} if path is not None and change["action"] == "create" else change
