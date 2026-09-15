"""One model document's contribution to the semantic index, remembered by `hash_c` so a
rebuild only extracts a document whose text moved (PLAN 15 M2): `doc_contribution` is what
`_walk_model` (semantic.py) calls per document, reusing the entry a previous walk recorded
for it — from the built cache, key mismatch and all — when its `hash_c` still matches."""

from __future__ import annotations

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.models import SemanticDocumentRecord
from sldb.store.semantic_doc_tags import tags_of as _tags_of


def process_doc(doc, doc_path, model_type, m_name, report, codec: StoreCodec = default_codec):
    report.docs_processed += 1
    doc.semantic_tags = list(_tags_of(doc, doc_path, model_type, m_name, codec))
    return SemanticDocumentRecord(model=m_name, path=doc.path, tags=doc.semantic_tags)


def doc_contribution(doc, d_path, cached, m_entry, resolver, py_path, report) -> dict:
    """One document's semantic entry: `cached` (from a previous walk) reused as-is when its
    `hash_c` still matches, otherwise extracted fresh."""
    if cached is not None and cached.get("hash_c") == doc.hash_c:
        doc.semantic_tags = list(cached["tags"])
        return dict(cached)
    rec = process_doc(doc, d_path, resolver(m_entry.model_ref, py_path), m_entry.name, report)
    return {"model": rec.model, "path": rec.path, "tags": rec.tags, "hash_c": doc.hash_c}
