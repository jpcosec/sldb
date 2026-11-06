"""Move a tracked document's Markdown file and keep it tracked under the same name."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_lookup import find_doc
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.transaction_paths import inside
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index


def move_document(store: str | Path | None, ref: str, new_path: str | Path, pythonpath: str | None = None) -> DocumentReference:
    """Move a document's file to `new_path` and re-track it under its current name.

    The document keeps its name and model, so edges pointing at it (`Model:name`) keep
    resolving; its derived indexes are rebuilt from the new path.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        ref: Document name, or its path as recorded in the store.
        new_path: Where the file goes; a relative path is relative to the project root, and
            the destination must stay inside it.
        pythonpath: Directory to import the store's model modules from.

    Returns:
        The document at its new path.

    Raises:
        SLDBError: When no model tracks such a document.
        SLDBStoreError: When `new_path` leaves the project root or a file already sits there;
            nothing is moved then.
    """
    location = open_store(store)
    m_entry, _, doc = find_doc(location.store_path, location.project_root, load_store_index(location.store_path), ref)
    target = _destination(location.project_root, new_path)
    untracked = untrack_document(location.store_path, doc.name, pythonpath)
    target.parent.mkdir(parents=True, exist_ok=True)
    untracked.path.rename(target)
    return track_document_file(location.store_path, m_entry.name, target, doc.name, pythonpath, force=True)


def _destination(root: Path, new_path: str | Path) -> Path:
    target = inside(root, new_path)
    if target.exists():
        raise SLDBStoreError(f"Cannot move to '{new_path}': a file already exists there.")
    return target
