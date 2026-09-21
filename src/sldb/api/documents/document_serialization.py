"""JSON projection of a RuntimeDocument: the API contract serializers live here, not in the CLI."""

from __future__ import annotations

from typing import Any


def serialize_document(doc: Any) -> dict[str, Any]:
    return {"id": doc.name, "model_name": doc.model_name, "path": str(doc.path), "version": doc_version(doc), "payload": doc.payload, "semantic_tags": doc.semantic_tags}


def doc_version(doc: Any) -> str | None:
    """The document's field hash (`hash_d`): the version token a client echoes back on save.

    `hash_d` is a pure function of the extracted payload, so it matches the payload
    equality the optimistic lock in /save uses, and rotates on every field write.
    """
    from sldb.api.journal import doc_hashes  # deferred: import-safe during package init

    return doc_hashes(doc.store_path, doc.model_name, doc.name)[1]