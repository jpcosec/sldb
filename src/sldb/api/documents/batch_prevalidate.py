"""Prevalidation of a batch before any write (`apply_batch`): shape, model, payload round-trip (G4),
guards, and targets (`_present`: a file to track; `_free`: a path inside the project, not taken)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_lookup import find_doc
from sldb.api.documents.payload_save_steps import model_class
from sldb.api.documents.transaction_paths import default_document_path, inside
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import ConflictError, SLDBError, SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.io import load_store_index
from sldb.store.query import load_runtime_documents

ACTIONS = ("create", "update", "move", "delete", "track", "untrack")


def prevalidate_changes(location: StoreLocation, changes: Any, pythonpath: str | None) -> list[dict[str, Any]]:
    """Every change checked in request order; the first problem raises, with nothing written."""
    if not isinstance(changes, list):
        raise SLDBValidationError("Expected a list of changes.")
    seen: set[str] = set()
    for change in changes:
        name = change.get("id") if isinstance(change, dict) else None
        if not isinstance(name, str) or name in seen or change.get("action") not in ACTIONS:
            raise SLDBValidationError(f"Invalid change (needs a unique string id and an action in {ACTIONS}): {change!r}")
        seen.add(name)
        _check(location, change, pythonpath)
    return changes


def _check(location: StoreLocation, change: dict[str, Any], pythonpath: str | None) -> None:
    existing = _existing(location, change["id"])
    if change["action"] in ("create", "track"):
        _check_new(location, change, existing, pythonpath)
    else:
        _check_tracked(location, change, existing, pythonpath)


def _existing(location: StoreLocation, name: str) -> tuple[Any, Any] | None:
    try:
        m_entry, _, doc = find_doc(location.store_path, location.project_root, load_store_index(location.store_path), name)
    except SLDBError:
        return None
    return m_entry, doc


def _check_new(location: StoreLocation, change: dict[str, Any], existing: tuple | None, pythonpath: str | None) -> None:
    if existing is not None:
        raise SLDBStoreError(f"Doc '{change['id']}' already tracked.")
    if not isinstance(change.get("model"), str):
        raise SLDBValidationError(f"{change['id']}: model must be a registered model name.")
    registered = load_registered_model(location.store_path, change["model"], pythonpath)
    if change["action"] == "track":
        _present(location, change)
        return
    _free(location, change, default_document_path(location.store_path, location.project_root, registered.entry.name, change["id"]))
    check_roundtrip(registered.model_type, change, location.project_root)


def _check_tracked(location: StoreLocation, change: dict[str, Any], existing: tuple | None, pythonpath: str | None) -> None:
    if existing is None:
        raise SLDBStoreError(f"Doc '{change['id']}' not found.")
    m_entry, doc = existing
    check_guards(location, m_entry, doc, change.get("expected_source_hash"), change.get("expected"), pythonpath)
    if change.get("model") not in (None, m_entry.name):
        raise SLDBValidationError(f"{change['id']}: a document cannot change model.")
    if change["action"] == "update":
        check_roundtrip(model_class(m_entry.model_ref, pythonpath, location.project_root), change, location.project_root)
    elif change["action"] == "move":
        _free(location, change, None)


def _present(location: StoreLocation, change: dict[str, Any]) -> None:
    if not isinstance(change.get("path"), str) or not inside(location.project_root, change["path"]).is_file():
        raise SLDBStoreError(f"{change['id']}: no file to track at {change.get('path')!r}.")


def _free(location: StoreLocation, change: dict[str, Any], default: Path | None) -> None:
    if change.get("path") is None and default is None:
        raise SLDBStoreError(f"{change['id']}: a path is required.")
    target = inside(location.project_root, change["path"]) if change.get("path") is not None else default
    if target.exists():
        raise SLDBStoreError(f"{change['id']}: file {target} already exists.")


def check_roundtrip(model_type: type, change: dict[str, Any], root: Path) -> None:
    """The payload must be an object the model renders and reads back identically (G4)."""
    payload = change.get("payload")
    if not isinstance(payload, dict):
        raise SLDBValidationError(f"{change['id']}: payload must be an object.")
    try:
        valid, details = validate_model_input_roundtrip(model_type, render_model_markdown(model_type, payload, root))
    except Exception as exc:
        raise SLDBValidationError(f"{change['id']}: {exc}") from exc
    if not valid:
        raise SLDBValidationError(f"{change['id']}: payload does not round-trip under {model_type.__name__}.", details)


def check_guards(location: StoreLocation, m_entry: Any, doc: Any, expected_source_hash: str | None, expected: Any, pythonpath: str | None) -> None:
    """`expected_source_hash` first, then `expected` against the current payload (q15)."""
    if expected_source_hash is not None and doc.source_hash != expected_source_hash:
        raise ConflictError(doc.name, expected_source_hash, doc.source_hash)
    if expected is not None:
        actual = current_payload(location, m_entry.name, doc.name, pythonpath)
        if actual != expected:
            raise ConflictError(doc.name, expected, actual)


def current_payload(location: StoreLocation, model: str, name: str, pythonpath: str | None) -> Any:
    docs = load_runtime_documents(location.store_path, resolve_model_ref, pythonpath)
    return next((d.payload for d in docs if d.model_name == model and d.name == name), None)
