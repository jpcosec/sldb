"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.journal import doc_address, doc_hashes, record, store_hash
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document


def create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None = None, pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Write the Markdown a model renders from `payload` and start tracking it.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file to write (parents are created, an existing file is
            overwritten); a relative path is relative to the project root, not the cwd.
        payload: The document's field values; it has no fixed schema beyond the model's own.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        actor: Optional label recorded in the store journal for this write.

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
    doc_path = _resolve_path(path, location.project_root)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(rendered + "\n", encoding="utf-8")
    doc_name = name or doc_path.stem
    _track_and_record(location.store_path, location.project_root, registered, doc_path, doc_name, payload, pythonpath, actor)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    raw_path = Path(raw)
    return raw_path.resolve() if raw_path.is_absolute() else (root / raw_path).resolve()


def _track_and_record(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, payload: dict[str, Any], pythonpath: str | None, actor: str | None) -> None:
    before = store_hash(sp)
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    hash_c, hash_d = doc_hashes(sp, registered.entry.name, doc_name)
    record(sp, {"operation": "create_document", "address": doc_address(registered.entry.name, doc_name), "new_value": payload, "hash_c_after": hash_c, "hash_d_after": hash_d, "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})


def _render_roundtrip(model_type: type, payload: dict[str, Any]) -> str:
    """The payload rendered to Markdown, refused unless it extracts back identically."""
    rendered = render_model_markdown(model_type, payload)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
    return rendered
