"""Start tracking an existing Markdown file as a document of a registered model."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.ops import track_document


def track_document_file(store: str | Path | None, model_name: str, path: str | Path, name: str | None = None, pythonpath: str | None = None, force: bool = False) -> DocumentReference:
    """Index a Markdown file as a document of a model.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file; a relative path is relative to the project root, not the cwd.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        force: Track without checking that the file round-trips under the model.

    Returns:
        The tracked document.

    Raises:
        SLDBStoreError: When the model is not registered.
        SLDBValidationError: When the file does not round-trip and `force` is False.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    raw = Path(path)
    doc_path = raw.resolve() if raw.is_absolute() else (location.project_root / raw).resolve()
    if not force:
        _check_roundtrip(registered.model_type, doc_path)
    doc_name = name or doc_path.stem
    track_document(location.store_path, location.project_root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _check_roundtrip(model_type: type, doc_path: Path) -> None:
    """Refuse a file that does not extract and re-render identically under the model."""
    valid, details = validate_model_input_roundtrip(model_type, doc_path.read_text(encoding="utf-8"))
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
