"""The semantic tags of one document, remembered by (absolute path, source_hash, model class) so a
rebuild only extracts documents whose text moved in the hash chain; the payload comes from the
runtime document cache when it already holds it.

The key used to be (relative path, source_hash, model *name*). Two stores with a `d.md` of the same
text under two different classes named `Spec` got one entry, and the second store carried the
first one's tags; so did a model whose `__semantics__` changed in a long-running process
without its documents' text changing. Tags are what a class makes of a text: the class is the
key, not its name.

A document its model rejects keeps the tags it last had: reading it as an empty payload dropped
the tags its fields carried, and every rebuild of the model rewrote its versioned shard without
them (inbox 3895e9f7, H3); `stores check` names it as `store/doc-invalid`."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.semantic_tags import collect_document_semantic_tags
from sldb.store.source_read import read_source_text

_DOC_TAGS: dict[tuple, list[str]] = {}


def _extract_tags(doc, doc_path: Path, model_type, m_name: str, codec: StoreCodec) -> list[str] | None:
    """The tags `model_type` makes of the document; None when the model rejects its text."""
    from sldb.store.runtime_cache import payload_of
    payload = payload_of(doc.path, doc.hash_c, model_type) if codec is default_codec else None
    if payload is None:
        try:
            payload = codec.extract(model_type, read_source_text(doc_path))
        except ValidationError:
            return None
        except Exception:  # noqa: BLE001 - an unreadable document has no tags of its own
            payload = {}
    return collect_document_semantic_tags(model_type, payload)


def tags_of(doc, doc_path: Path, model_type, m_name: str, codec: StoreCodec = default_codec) -> list[str]:
    key = (str(doc_path), doc.hash_c, model_type)
    tags = _DOC_TAGS.get(key) if codec is default_codec else None
    if tags is None:
        tags = _extract_tags(doc, doc_path, model_type, m_name, codec)
        if tags is None:
            return list(doc.semantic_tags)  # rejected by its model: the tags it last had (inbox 3895e9f7 H3)
        if codec is default_codec:
            _DOC_TAGS[key] = tags
    return tags
