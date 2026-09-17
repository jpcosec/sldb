"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document


def create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None = None, pythonpath: str | None = None) -> DocumentReference:
    """Write the Markdown a model renders from `payload` and start tracking it.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file to write (parents are created, an existing file is
            overwritten); a relative path is relative to the project root, not the cwd.
        payload: The document's field values; it has no fixed schema beyond the model's own.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.

    Returns:
        The created document.

    Raises:
        SLDBStoreError: When the model is not registered.
        SLDBValidationError: When the rendered Markdown does not round-trip under the model;
            nothing is written then.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    rendered = _render_roundtrip(registered.model_type, payload)
    raw = Path(path)
    doc_path = raw.resolve() if raw.is_absolute() else (location.project_root / raw).resolve()
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(rendered + "\n", encoding="utf-8")
    doc_name = name or doc_path.stem
    track_document(location.store_path, location.project_root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _render_roundtrip(model_type: type, payload: dict[str, Any]) -> str:
    """The payload rendered to Markdown, refused unless it extracts back identically."""
    rendered = render_model_markdown(model_type, payload)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
    return rendered
