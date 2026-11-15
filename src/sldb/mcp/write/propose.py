"""The dry run: typed changes into a batch with the server's guards, and what it would write."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import document_address
from sldb.mcp.changes import AssertEdge, BatchChange, CreateDocument, UpdateDocument, edge_payload, model_of


def create_change(store_path: Path, change: CreateDocument | AssertEdge) -> BatchChange:
    """A new document, or the RelationDoc of an asserted edge."""
    model = model_of(change)
    if not api.is_model_registered(store_path, model):
        raise ValueError(f"{model} is not a model this store registers; list_models names them")
    payload = change.payload if isinstance(change, CreateDocument) else edge_payload(change)
    return BatchChange(id=change.name, action="create", model=model, payload=payload, path=change.path)


def updated_payload(store_path: Path, change: UpdateDocument) -> dict[str, Any]:
    """The document's payload with the fields of the change set."""
    payload = copy.deepcopy(api.runtime_document(store_path, None, f"{change.model}/{change.name}").payload)
    for path, value in change.fields.items():
        api.deep_set(payload, path, value, create=True)
    return payload


def existing_change(store_path: Path, change: Any, fingerprint: Any) -> BatchChange:
    """An update, a delete or a retracted edge: guarded by the document's source hash."""
    model, name = model_of(change), change.name
    hashes = fingerprint.documents.get(f"{model}:{name}")
    if hashes is None:
        raise ValueError(f"{model}:{name} is not a document of this store (a linked store's documents are not written through it)")
    if isinstance(change, UpdateDocument):
        return BatchChange(id=name, action="update", model=model, payload=updated_payload(store_path, change), expected_source_hash=hashes.source_hash)
    return BatchChange(id=name, action="delete", model=model, expected_source_hash=hashes.source_hash)


def batch_change(store_path: Path, change: Any, fingerprint: Any) -> BatchChange:
    """The batch entry a typed change becomes."""
    if isinstance(change, (CreateDocument, AssertEdge)):
        return create_change(store_path, change)
    return existing_change(store_path, change, fingerprint)


def changed_fields(store_path: Path, change: BatchChange) -> dict[str, Any]:
    """The payload an update would write and the fields that differ from the stored one."""
    before, after = api.runtime_document(store_path, None, f"{change.model}/{change.id}").payload, change.payload or {}
    return {"payload": change.payload, "changed_fields": sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))}


def would_write(store_path: Path, change: BatchChange) -> dict[str, Any]:
    """What one change of the batch would write."""
    export_id = f"{change.model}:{change.id}"
    row = {"action": change.action, "export_id": export_id, "address": document_address(export_id), "model": change.model}
    if change.action == "create":
        return {**row, "path": change.path, "payload": change.payload}
    row = {**row, "path": api.doc_status(store_path, f"{change.model}/{change.id}").path, "expected_source_hash": change.expected_source_hash}
    return row if change.action == "delete" else {**row, **changed_fields(store_path, change)}
