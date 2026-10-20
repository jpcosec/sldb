"""Rehash every tracked document of a store whose Markdown changed since it was indexed.

Moved here from `sldb.cli.commands.store_update`, which re-exports these names.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.document_field_hashes import _field_hash, _field_hashes  # noqa: F401 - re-exported
from sldb.models.provenance_block import index_block
from sldb.store.hashing import hash_text
from sldb.store.field_set_drift import signed_under_other_fields
from sldb.store.model_node import contract_moved
from sldb.store.io import load_documents_index, load_models_index
from sldb.store.models.store_index import StoreIndex


def _process_models(idx: StoreIndex, root: Path, pypath: str | None, skipped_models: list[str], skipped_docs: list[str], pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    """Rehash every model's documents; a model whose class fails to import is recorded as skipped.

    The broad catch isolates one broken model module (it may raise anything on import)
    from the rest of the store, and records it in `skipped_models` for the report. Its
    documents are not rehashed, but its roster still is: see `_queue_roster_only`.
    """
    for m_entry in idx.models:
        try:
            mtype = resolve_model_ref(m_entry.model_ref, pypath)
            _process_model(m_entry, mtype, root, skipped_docs, pending, changed)
        except Exception:
            skipped_models.append(m_entry.name)
            changed.pop(m_entry.name, None)
            _queue_roster_only(m_entry, root, pending)


def _queue_roster_only(m_entry: Any, root: Path, pending: list[tuple[Any, Any, Any, Any]]) -> None:
    """Queue a skipped model with no class, so the commit re-signs its roster and count.

    Skipping the model whole left a stale roster as `roster stale` in `stores check` for
    good. The indexes are reloaded, dropping anything a failed pass half changed;
    `stamp_model_node` with no class keeps the contract the model signed.
    """
    try:
        m_idx = load_models_index(root / m_entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
    except Exception:
        return
    pending.append((m_entry, m_idx, d_idx, None))


def _process_model(m_entry: Any, mtype: Any, root: Path, skipped_docs: list[str], pending: list[tuple[Any, Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    """Rehash one model's documents and queue its indexes to be saved.

    A contract that moved forces every document of the model through extraction again, even
    where the Markdown is untouched: a field added to the class, or a changed template, makes
    the same text yield a different payload, and no `source_hash` moves to say so.
    """
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    force = contract_moved(m_idx, mtype)
    for doc in d_idx.documents:
        if _process_doc(doc, mtype, m_entry.name, root, skipped_docs, force):
            changed.setdefault(m_entry.name, []).append(doc)
    pending.append((m_entry, m_idx, d_idx, mtype))


def _process_doc(doc: Any, mtype: Any, m_name: str, root: Path, skipped_docs: list[str], force: bool = False) -> bool:
    """Rehash one document when its Markdown or its stored hashes say it needs it.

    A hand edit is only ever seen by re-reading the file (source_hash), unavoidably, for every
    tracked document — but PLAN 15 capa 8: the expensive part, extracting content_hash, only
    runs for a document whose source_hash actually moved since the per-document hash map last
    knew it. `force` is the one case where the text is not the trigger: the model's contract
    moved, so the payload can change with the text standing still.
    """
    doc_path = root / doc.path
    if not doc_path.exists():
        skipped_docs.append(doc.name)
        return False
    text = doc_path.read_text(encoding="utf-8")
    fresh = hash_text(text)
    force = force or signed_under_other_fields(doc.field_hashes, mtype)  # see sldb.store.field_set_drift
    if _trusted(doc, fresh, force):
        return False
    return _restamp(doc, mtype, m_name, text, fresh, force)


def _trusted(doc: Any, fresh: str, force: bool) -> bool:
    """Whether the stored hashes are enough to skip re-extraction for unchanged text.

    A matching source_hash is not enough on its own: a shard written before per-field hashes
    existed carries a content_hash nothing verified, and `migrate_hash_names` renames that key
    without recomputing it, so trusting it kept a stale content_hash (and a permanent
    `data_mutation` in `stores check`) forever, with the Markdown intact. A present field_hashes
    map is the evidence that a content_hash came out of the current pipeline; its absence sends
    the document through extraction once, which both validates the hash and backfills the map.
    """
    return not force and fresh == doc.source_hash and bool(doc.field_hashes)


def _restamp(doc: Any, mtype: Any, m_name: str, text: str, fresh: str, force: bool) -> bool:
    """Re-extract and store the hashes; False when they came back identical (nothing moved).

    `doc.source_hash` is updated before extracting on purpose: the extraction cache is keyed
    on the source hash the payload belongs to, so passing the old one here would read another
    document's cached payload (the file's previous content) and sign a wrong content_hash.
    """
    previous = (doc.source_hash, doc.content_hash, doc.field_hashes, doc.provenance)
    doc.source_hash = fresh
    doc.content_hash, doc.field_hashes, doc.provenance = *_field_hashes(mtype, m_name, doc, text, force), index_block(text)
    return (doc.source_hash, doc.content_hash, doc.field_hashes, doc.provenance) != previous
