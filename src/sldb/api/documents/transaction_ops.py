"""The operations of a `Transaction`: each one the public function it names, with the files it
may move snapshotted first so the transaction's rollback can put them back."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.api.documents.batch_prevalidate import check_guards
from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents.document_lookup import find_doc
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.move_document import move_document
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.transaction_paths import default_document_path, document_files
from sldb.api.documents.transaction_state import TransactionState
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.core.exceptions import ConflictError
from sldb.store.io import load_store_index
from sldb.store.source_guard import read_source_bytes, write_source_bytes


def create(state: TransactionState, model: str, name: str, payload: dict[str, Any], path: str | Path | None) -> DocumentReference:
    registered = load_registered_model(state.store_path, model, state.pythonpath).entry.name
    target = state.inside(path) if path is not None else default_document_path(state.store_path, state.root, registered, name)
    _remember(state, registered, name, target)
    return create_document(state.store_path, model, target, payload, name, state.pythonpath)


def update(state: TransactionState, ref: str, payload: dict[str, Any], expected_source_hash: str | None, expected: Any) -> DocumentReference:
    m_entry, doc = _found(state, ref)
    check_guards(state.location, m_entry, doc, expected_source_hash, expected, state.pythonpath)
    _remember(state, m_entry.name, doc.name, state.root / doc.path)
    return save_document_payload(state.store_path, m_entry.name, doc.name, payload, state.pythonpath)


def delete(state: TransactionState, ref: str) -> DocumentReference:
    m_entry, doc = _found(state, ref)
    _remember(state, m_entry.name, doc.name, state.root / doc.path)
    return delete_document(state.store_path, doc.name, state.pythonpath)


def move(state: TransactionState, ref: str, new_path: str | Path) -> DocumentReference:
    m_entry, doc = _found(state, ref)
    target = state.inside(new_path)
    _remember(state, m_entry.name, doc.name, state.root / doc.path)
    state.remember([target])
    return move_document(state.store_path, doc.name, target, state.pythonpath)


def track(state: TransactionState, path: str | Path, model: str, name: str | None) -> DocumentReference:
    target = state.inside(path)
    registered = load_registered_model(state.store_path, model, state.pythonpath).entry.name
    _remember(state, registered, name or target.stem, None)
    return track_document_file(state.store_path, model, target, name, state.pythonpath)


def untrack(state: TransactionState, ref: str) -> DocumentReference:
    m_entry, doc = _found(state, ref)
    _remember(state, m_entry.name, doc.name, None)
    return untrack_document(state.store_path, doc.name, state.pythonpath)


def write_file(state: TransactionState, path: str | Path, data: bytes, expected_sha256: str | None) -> Path:
    """A plain file written in the transaction; with `expected_sha256`, only if its current
    bytes (None when absent) hash to it, else `ConflictError` and nothing is written."""
    target = state.inside(path)
    actual = hashlib.sha256(read_source_bytes(target)).hexdigest() if target.exists() or target.is_symlink() else None
    if expected_sha256 is not None and actual != expected_sha256:
        raise ConflictError(state.relative(target), expected_sha256, actual)
    state.remember([target])
    target.parent.mkdir(parents=True, exist_ok=True)
    write_source_bytes(target, data)  # O_NOFOLLOW: a symlink swapped in after the read is not written through
    return target


def record(state: TransactionState, path: str | Path) -> Path:
    """Snapshot a file the caller writes on its own, so the rollback restores it too."""
    target = state.inside(path)
    state.remember([target])
    return target


def _found(state: TransactionState, ref: str) -> tuple[Any, Any]:
    m_entry, _, doc = find_doc(state.store_path, state.root, load_store_index(state.store_path), ref)
    return m_entry, doc


def _remember(state: TransactionState, model: str, name: str, doc_path: Path | None) -> None:
    state.remember(document_files(state.store_path, state.root, model, name, doc_path), model)
