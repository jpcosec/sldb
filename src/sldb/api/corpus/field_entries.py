"""Reading one store's documents into per-field corpus entries.

The hash of an entry is the field's own (`DocumentEntry.field_hashes`), so a re-index
embeds the fields that moved and reuses the rest.
"""

from __future__ import annotations

from typing import Any

from sldb.api.corpus.corpus_entries import export_id
from sldb.api.corpus.field_entry import FieldEntry
from sldb.api.corpus.document_context import DocumentContext
from sldb.api.corpus.field_hit import FieldHit
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.hashing import hash_payload
from sldb.store.query import load_runtime_documents

LOCAL = "local"


def field_entries(corpus) -> list[FieldEntry]:
    """Every field of every admitted document that the field projection admits."""
    records = load_runtime_documents(
        corpus.store, resolve_model_ref, corpus.pythonpath, include_linked=True
    )
    entries: list[FieldEntry] = []
    for record in records:
        entries.extend(_entries_of(corpus, record))
    return entries


def _entries_of(corpus, record: Any) -> list[FieldEntry]:
    context = _context(corpus, record)
    if context is None:
        return []
    payload = (record.payload or {}).items()
    return [e for name, value in payload if (e := _entry(corpus, context, name, value))]


def _context(corpus, record: Any) -> DocumentContext | None:
    """The shared identity of a document's fields, or None when the corpus excludes it."""
    model = record.model_name or ""
    store = None if record.store_name == LOCAL else record.store_name
    if not _admits(corpus, model, store):
        return None
    document_id = export_id(record.store_name, model, record.name)
    return DocumentContext(record, model, store, document_id, _field_hashes(record))


def _admits(corpus, model: str, store: str | None) -> bool:
    if not corpus.projection.admits(model):
        return False
    return corpus.projection.stores is None or store in corpus.projection.stores


def _field_hashes(record: Any) -> dict[str, str]:
    """The record's per-field hashes, recomputed when the store never recorded them.

    An empty map means the store predates `field_hashes` (or the document no longer
    extracts), never that no field has a hash. Falling back to hashing the payload in
    memory keeps a per-field index usable against an un-migrated store — at the cost of
    hashing on read — instead of leaving every entry unhashed and re-embedding everything
    on every refresh.
    """
    recorded = dict(getattr(record, "field_hashes", {}) or {})
    if recorded:
        return recorded
    return {name: hash_payload(value) for name, value in (record.payload or {}).items()}


def _entry(corpus, context: DocumentContext, name: str, value: Any) -> FieldEntry | None:
    if not corpus.field_projection.admits(name):
        return None
    text = corpus.field_projection.text_of(value)
    return context.entry(name, text) if text else None


def select_field_hits(ranked, by_id, allowed: set[str] | None, k: int | None) -> list[FieldHit]:
    """The ranked fields still in the corpus (and among the allowed ones), at most k.

    `allowed` admits a field by its own id or by its document's: narrowing to a document
    means every field of it, which is what a caller filtering by document intends.
    """
    hits: list[FieldHit] = []
    for entry_id, score in ranked:
        entry = by_id.get(entry_id)
        if entry is None or not _is_allowed(entry, entry_id, allowed):
            continue
        hits.append(FieldHit.of(entry, score))
        if k is not None and len(hits) >= k:
            break
    return hits


def _is_allowed(entry: FieldEntry, entry_id: str, allowed: set[str] | None) -> bool:
    return allowed is None or entry_id in allowed or entry.document_id in allowed
