"""The semantic tags of one document, remembered by (absolute path, hash_c, model class) so a
rebuild only extracts documents whose text moved in the hash chain; the payload comes from the
runtime document cache when it already holds it.

The key used to be (relative path, hash_c, model *name*). Two stores with a `d.md` of the same
text under two different classes named `Spec` got one entry, and the second store carried the
first one's tags; so did a model whose `__semantics__` changed in a long-running process
without its documents' text changing. Tags are what a class makes of a text: the class is the
key, not its name."""

from __future__ import annotations

from pathlib import Path

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.semantic_tags import collect_document_semantic_tags

_DOC_TAGS: dict[tuple, list[str]] = {}


def _extract_tags(doc, doc_path: Path, model_type, m_name: str, codec: StoreCodec) -> list[str]:
    from sldb.store.runtime_cache import payload_of
    payload = payload_of(doc.path, doc.hash_c, model_type) if codec is default_codec else None
    if payload is None:
        try:
            payload = codec.extract(model_type, doc_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - an unreadable document has no tags of its own
            payload = {}
    return collect_document_semantic_tags(model_type, payload)


def tags_of(doc, doc_path: Path, model_type, m_name: str, codec: StoreCodec = default_codec) -> list[str]:
    key = (str(doc_path), doc.hash_c, model_type)
    tags = _DOC_TAGS.get(key) if codec is default_codec else None
    if tags is None:
        tags = _extract_tags(doc, doc_path, model_type, m_name, codec)
        if codec is default_codec:
            _DOC_TAGS[key] = tags
    return tags
