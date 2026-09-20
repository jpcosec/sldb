"""Write a whole payload back to a tracked document: render, round-trip, rehash, reindex."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.payload_save_steps import load_document_entry, load_model_indexes, model_class, render_checked, save_document_indexes, write_rendered_document
from sldb.api.journal import doc_address, record, store_hash
from sldb.api.stores.open_store import open_store
from sldb.store.codec import default_codec


def save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Replace a tracked document's content with the Markdown rendered from `payload`.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        model_name: Registered model name of the document.
        document_name: Tracked document name.
        payload: The complete new payload; it has no fixed schema beyond the model's own.
        pythonpath: Directory to import the model module from; the store's project root
            is tried next, since a linked store's models import from where it lives.
        actor: Optional label recorded in the store journal for this write.

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
    _save_and_record(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor)
    return DocumentReference(model=m_entry.name, name=doc_entry.name, path=location.project_root / doc_entry.path)


def _save_and_record(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor) -> None:
    before_a = store_hash(location.store_path)
    previous = _old_payload(location.project_root, doc_entry, model_type)
    hash_c_before, hash_d_before = doc_entry.hash_c, doc_entry.hash_d
    write_rendered_document(location.project_root, doc_entry, model_type, render_checked(model_type, payload))
    save_document_indexes(location.store_path, location.project_root, idx, m_idx, m_entry, doc_entry, pythonpath)
    record(location.store_path, {"operation": "save_document_payload", "address": doc_address(m_entry.name, doc_entry.name), "previous_value": previous, "new_value": payload, "hash_c_before": hash_c_before, "hash_c_after": doc_entry.hash_c, "hash_d_before": hash_d_before, "hash_d_after": doc_entry.hash_d, "hash_a_before": before_a, "hash_a_after": store_hash(location.store_path), "actor": actor})


def _old_payload(root: Path, doc_entry, model_type: type) -> Any | None:
    try:
        text = (root / doc_entry.path).read_text(encoding="utf-8")
        return default_codec.extract(model_type, text)
    except Exception:
        return None
