"""One document's semantic shard (PLAN 15 capa 5): the shard itself, keyed by `source_hash`, is
now the cache — a document whose `source_hash` matches what its shard already says is left
untouched; a new or changed one is extracted and its shard (re)written, on its own, no other
document's shard is read or rewritten.

A model whose class does not import here (deleted, or its package absent) is skipped and named
in `report.models_unresolved`: the document keeps the tags its shard already had, if any, so a
rebuild never fails on a model nobody is reading."""

from __future__ import annotations

from sldb.store.exceptions import SLDBModelError
from sldb.store.codec import StoreCodec, default_codec
from sldb.store.io.shards import load_semantic_shard, save_semantic_shard
from sldb.store.layout import semantic_shard_path
from sldb.store.models import SemanticDocumentRecord
from sldb.store.semantic_doc_tags import tags_of as _tags_of


def process_doc(doc, doc_path, model_type, m_name, report, codec: StoreCodec = default_codec) -> SemanticDocumentRecord:
    report.docs_processed += 1
    doc.semantic_tags = list(_tags_of(doc, doc_path, model_type, m_name, codec))
    return SemanticDocumentRecord(model=m_name, path=doc.path, tags=doc.semantic_tags, source_hash=doc.source_hash)


def sync_doc_shard(store_path, doc, d_path, m_entry, resolver, py_path, report) -> SemanticDocumentRecord:
    """This document's semantic shard, current: reused untouched when its `source_hash` already
    matches what the shard on disk carries, (re)extracted and (re)written otherwise."""
    path = semantic_shard_path(store_path, m_entry.name, doc.name)
    cached = load_semantic_shard(path)
    if cached is not None and cached.source_hash == doc.source_hash:
        doc.semantic_tags = list(cached.tags)
        return cached
    if (model_type := _resolve(resolver, m_entry.model_ref, py_path)) is None:
        return _unresolved(doc, m_entry.name, cached, report)
    rec = process_doc(doc, d_path, model_type, m_entry.name, report)
    save_semantic_shard(path, rec)
    return rec


def _resolve(resolver, model_ref: str, py_path):
    try:
        return resolver(model_ref, py_path)
    except SLDBModelError:
        return None


def _unresolved(doc, m_name: str, cached: SemanticDocumentRecord | None, report) -> SemanticDocumentRecord:
    """The document's last known tags, unchanged and unwritten; the model named once."""
    if m_name not in report.models_unresolved:
        report.models_unresolved.append(m_name)
    tags = list(cached.tags) if cached is not None else list(doc.semantic_tags)
    return SemanticDocumentRecord(model=m_name, path=doc.path, tags=tags, source_hash=doc.source_hash)
