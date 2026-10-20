"""JSON projection of a RuntimeDocument: the API contract serializers live here, not in the CLI."""

from __future__ import annotations

from typing import Any


def serialize_document(doc: Any) -> dict[str, Any]:
    return {"id": doc.name, "model_name": doc.model_name, "path": str(doc.path), "version": doc_version(doc), "payload": doc.payload, "semantic_tags": doc.semantic_tags, "provenance": provenance(doc)}


def provenance(doc: Any) -> dict[str, Any]:
    """The document's `sldb` block as read from its file now, or the defaults (`declared: false`)."""
    from pathlib import Path

    from sldb.api.documents.provenance_stamp import provenance_of
    from sldb.store.layout import project_root

    path = Path(doc.path) if Path(doc.path).is_absolute() else project_root(Path(doc.store_path)) / doc.path
    found = provenance_of(path.read_text(encoding="utf-8")) if path.is_file() else provenance_of("")
    return {**found.model_dump(by_alias=True), "declared": found.declared}


def doc_version(doc: Any) -> str | None:
    """The document's field hash (`content_hash`): the version token a client echoes back on save.

    `content_hash` is a pure function of the extracted payload, so it matches the payload
    equality the optimistic lock in /save uses, and rotates on every field write.
    """
    from sldb.api.journal import doc_hashes  # deferred: import-safe during package init

    return doc_hashes(doc.store_path, doc.model_name, doc.name)[1]