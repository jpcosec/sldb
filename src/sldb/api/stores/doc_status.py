"""Does a document reference resolve? Answered from the stores' indexes, without importing it.

Asking never writes: the store asked from gains no entry, model or hash for the documents it
references (they stay trackable there, not tracked).
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.doc_ref import LOCAL, matches_doc_ref, qualifier, split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_links import find_link


def doc_status(store: str | Path | None, ref: str) -> DocRefStatus:
    """The state of `ref` read from `store`: `ok`, `missing`, `ambiguous`, `link-missing` or `link-broken`.

    Args:
        store: The store the reference is written in (path, alias, or None to discover it).
        ref: `name`, `Model/name` or a tracked path, optionally behind `alias:` (see `doc_ref`).
    """
    store_path = open_store(store, mode="readonly").store_path
    alias, rest = split_doc_ref(store_path, ref)
    if alias is not None:
        return _linked_status(store_path, ref, alias, rest)
    found = _lookup(store_path, ref, LOCAL, rest)
    prefix = qualifier(ref)
    if found.status == "missing" and prefix not in (None, LOCAL):
        return DocRefStatus(ref=ref, store=prefix, status="link-missing", detail=f"no linked store named '{prefix}'")
    return found


def doc_exists(store: str | Path | None, ref: str) -> bool:
    """True when `ref` names exactly one document (see `doc_status` for why it may not)."""
    return doc_status(store, ref).exists


def _linked_status(store_path: Path, ref: str, alias: str, rest: str) -> DocRefStatus:
    link = find_link(store_path, alias)
    if link["status"] != "ok":
        return DocRefStatus(ref=ref, store=alias, status="link-broken", detail=f"link '{alias}' is {link['status']}: {link['resolved']}")
    return _lookup(Path(link["resolved"]), ref, alias, rest)


def _lookup(store_path: Path, ref: str, store_name: str, rest: str) -> DocRefStatus:
    hits = [d for d in indexed_documents(store_path) if matches_doc_ref(rest, d["name"], d["path"], d["model"])]
    if len(hits) == 1:
        return DocRefStatus(ref=ref, store=store_name, status="ok", **hits[0])
    if hits:
        return DocRefStatus(ref=ref, store=store_name, status="ambiguous", detail="use 'Model/name' or a tracked path")
    return DocRefStatus(ref=ref, store=store_name, status="missing")
