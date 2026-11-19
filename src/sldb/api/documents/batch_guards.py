"""The guards a batch change can carry, checked against the document's current state before a write:
`expected_source_hash`, `expected_content_hash` (the text without its provenance block) and
`expected` (the current payload)."""

from __future__ import annotations

from typing import Any

from sldb.api.documents.content_hash import document_content_hash
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import ConflictError
from sldb.store.query import load_runtime_documents


def check_guards(location: StoreLocation, m_entry: Any, doc: Any, expected_source_hash: str | None, expected: Any, pythonpath: str | None, expected_content_hash: str | None = None) -> None:
    """`expected_source_hash` first, then `expected_content_hash` (the text without its provenance
    block), then `expected` against the current payload (q15)."""
    if expected_source_hash is not None and doc.source_hash != expected_source_hash:
        raise ConflictError(doc.name, expected_source_hash, doc.source_hash)
    if expected_content_hash is not None:
        actual_hash = document_content_hash(location, doc)
        if actual_hash != expected_content_hash:
            raise ConflictError(doc.name, expected_content_hash, actual_hash)
    if expected is not None:
        actual = current_payload(location, m_entry.name, doc.name, pythonpath)
        if actual != expected:
            raise ConflictError(doc.name, expected, actual)


def current_payload(location: StoreLocation, model: str, name: str, pythonpath: str | None) -> Any:
    docs = load_runtime_documents(location.store_path, resolve_model_ref, pythonpath)
    return next((d.payload for d in docs if d.model_name == model and d.name == name), None)
