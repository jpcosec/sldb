"""Which of many references name a tracked document: `doc_status` asked once for all of them.

The store's documents index is read once and looked up for every reference, instead of one
`doc_status` (one index read) per reference. A reference behind a store qualifier is still
asked to `doc_status`, which knows the links.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.stores.doc_ref import qualifier
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_status
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.api.stores.open_store import open_store


def tracked_documents(store: str | Path | None, refs: Iterable[str]) -> dict[str, DocRefStatus]:
    """`{ref: status}` of the references `doc_status` would report `ok`, the others left out.

    Args:
        store: The store the references are read from (path, alias, or None to discover it).
        refs: `name`, `Model/name` or tracked paths, optionally behind `alias:`.

    Returns:
        The status of each reference that names exactly one document.
    """
    store_path = open_store(store, mode="readonly").store_path
    documents = indexed_documents(store_path)
    hits = _hits_by_ref(documents)
    found: dict[str, DocRefStatus] = {}
    for ref in refs:
        status = _status(store_path, ref, hits, documents)
        if status is not None and status.exists:
            found[ref] = status
    return found


def _hits_by_ref(documents: list[dict[str, str]]) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {}
    for position, document in enumerate(documents):
        for key in {document["name"], document["path"], f"{document['model']}/{document['name']}"}:
            hits.setdefault(key, []).append(position)
    return hits


def _status(store_path: Path, ref: str, hits: dict[str, list[int]], documents: list[dict[str, str]]) -> DocRefStatus | None:
    if qualifier(ref) is not None:
        return doc_status(store_path, ref)
    found = hits.get(ref.strip("/"), [])
    return DocRefStatus(ref=ref, store="local", status="ok", **documents[found[0]]) if len(found) == 1 else None
