"""Delete a tracked document: untrack it AND remove its Markdown file, leaving no residue."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.untrack_document import untrack_document
from sldb.store import runtime_cache_disk


def delete_document(store: str | Path | None, document: str, pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Untrack a document and delete the Markdown file it was tracking.

    `untrack_document` is the half of this that keeps the file: it drops the document
    from the store indexes and leaves the Markdown alone, which is what you want when a
    document should stop being tracked but stay on disk. When the document should be
    gone, untracking alone leaves the file behind, and re-tracking the store picks it up
    again. This deletes both, and purges the extraction cache entry that would otherwise
    keep describing a file that no longer exists.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        document: Document name, or its path as recorded in the store.
        pythonpath: Directory to import the store's model modules from.
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The document that was deleted, including the path the file used to have.

    Raises:
        SLDBError: When no model tracks such a document.
    """
    deleted = untrack_document(store, document, pythonpath=pythonpath, actor=actor)
    deleted.path.unlink(missing_ok=True)
    _forget_cached_extraction(deleted)
    return deleted


def _forget_cached_extraction(deleted: DocumentReference) -> None:
    """Drop the cache entries whose leaf key names the deleted file.

    The cache is keyed by path, hash and model, so a deleted document leaves a stale
    entry until a full load rewrites the file. Harmless for correctness (the payload is
    never served for a document the store no longer tracks) but it keeps a deleted path
    in a file that is read as a description of the store.
    """
    store_path = _store_path_of(deleted.path)
    if store_path is None:
        return
    suffix, name = f"|{deleted.model}", deleted.path.name
    runtime_cache_disk.forget(store_path, lambda key: key.endswith(suffix) and key.split("|", 1)[0].endswith(name))


def _store_path_of(doc_path: Path) -> Path | None:
    """The `.sldb` directory above a document path, if there is one."""
    for parent in doc_path.parents:
        if (parent / ".sldb").is_dir():
            return parent / ".sldb"
    return None
