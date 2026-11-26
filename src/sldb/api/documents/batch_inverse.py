"""The batch that undoes a batch (`BatchReport.inverse`): `before` notes, under the store lock and
before the transaction, what each change will replace; `inverse` turns that, after the writes and
still under the lock, into changes `apply_batch` accepts. Every change over a document the batch
left tracked is guarded by the `expected_content_hash` it left (the document without its provenance block), so undoing after someone else's
write is a `ConflictError` with nothing written; recreating a deleted document someone else
recreated is the prevalidation's `SLDBStoreError` (already tracked, or file exists).

It is built from payloads, not from the transaction's byte snapshots: a canonical document comes
back byte for byte, its front-matter provenance (`sldb.by/at/via`) aside, and the undo is written
and stamped like any other write: the contract is 'same content, provenance aside', and the
guard compares content, so a document that went back to the content the batch left is not stale."""

from __future__ import annotations

from typing import Any

from sldb.models.provenance_block import read_block

from sldb.api.documents.content_hash import document_content_hash
from sldb.api.documents.batch_guards import current_payload
from sldb.api.documents.document_lookup import find_doc
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBError
from sldb.store.io import load_store_index

_UNDO = {"create": "delete", "track": "untrack", "update": "update", "move": "move", "untrack": "track", "delete": "create"}
_CARRY = {"create": (), "track": (), "update": ("payload",), "move": ("path",), "untrack": ("model", "path"), "delete": ("model", "path", "payload")}
_GUARDED = ("create", "track", "update", "move")


def before(location: StoreLocation, plan: list[dict[str, Any]], pythonpath: str | None) -> list[dict[str, Any]]:
    """Per change, the document it will replace: model, path, payload (updates and deletes only)."""
    return [{"id": change["id"], "action": change["action"], **_prior(location, change, pythonpath)} for change in plan]


def inverse(location: StoreLocation, prior: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The changes that put back what `prior` noted, each guarded by the hash the batch left."""
    return [_undo(location, noted) for noted in reversed(prior)]


def documents(prior: list[dict[str, Any]], undo: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The journal's per-document record: the before-image and the content hash the batch left."""
    left = {u["id"]: u.get("expected_content_hash") for u in undo}
    return [{"id": n["id"], "action": n["action"], "before": _before_image(n), "after_hash": left.get(n["id"])} for n in prior]


def _before_image(noted: dict[str, Any]) -> dict[str, Any] | None:
    if "model" not in noted:
        return None  # the batch created it
    return {key: noted[key] for key in ("model", "path", "payload", "provenance") if key in noted}


def _prior(location: StoreLocation, change: dict[str, Any], pythonpath: str | None) -> dict[str, Any]:
    found = _tracked(location, change["id"])
    if found is None:
        return {}
    m_entry, doc = found
    noted = {"model": m_entry.name, "path": doc.path}
    if change["action"] in ("update", "delete"):
        noted["payload"] = current_payload(location, m_entry.name, doc.name, pythonpath)
        noted["provenance"] = read_block((location.project_root / doc.path).read_text(encoding="utf-8"))
    return noted


def _undo(location: StoreLocation, noted: dict[str, Any]) -> dict[str, Any]:
    action = noted["action"]
    undo = {"id": noted["id"], "action": _UNDO[action], **{key: noted[key] for key in _CARRY[action]}}
    if action in _GUARDED:  # the batch left it tracked: guard the undo with the hash it left
        undo["expected_content_hash"] = document_content_hash(location, _tracked(location, noted["id"])[1])
    return undo


def _tracked(location: StoreLocation, name: str) -> tuple[Any, Any] | None:
    try:
        m_entry, _, doc = find_doc(location.store_path, location.project_root, load_store_index(location.store_path), name)
    except SLDBError:
        return None
    return m_entry, doc
