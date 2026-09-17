"""Write a whole payload back to a tracked document: render, round-trip, rehash, reindex."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.payload_save_steps import load_document_entry, load_model_indexes, model_class, render_checked, save_document_indexes, write_rendered_document
from sldb.api.stores.open_store import open_store


def save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None = None) -> DocumentReference:
    """Replace a tracked document's content with the Markdown rendered from `payload`.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        model_name: Registered model name of the document.
        document_name: Tracked document name.
        payload: The complete new payload; it has no fixed schema beyond the model's own.
        pythonpath: Directory to import the model module from; the store's project root
            is tried next, since a linked store's models import from where it lives.

    Returns:
        The document written.

    Raises:
        SLDBPayloadSaveError: When the model or document is not registered, or the rendered
            Markdown does not round-trip back to the payload.
    """
    location = open_store(store)
    idx, m_entry, m_idx = load_model_indexes(location.store_path, location.project_root, model_name)
    doc_entry = load_document_entry(location.store_path, m_entry.name, document_name)
    model_type = model_class(m_entry.model_ref, pythonpath, location.project_root)
    write_rendered_document(location.project_root, doc_entry, model_type, render_checked(model_type, payload))
    save_document_indexes(location.store_path, location.project_root, idx, m_idx, m_entry, doc_entry, pythonpath)
    return DocumentReference(model=m_entry.name, name=doc_entry.name, path=location.project_root / doc_entry.path)
