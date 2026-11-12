"""Start tracking an existing Markdown file as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.on_write_gate import check_entering_text
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.stores.policy import Policy
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.ops import track_document
from sldb.store.source_read import read_source_text, refuse_unreadable


def track_document_file(store: str | Path | None, model_name: str, path: str | Path, name: str | None = None, pythonpath: str | None = None, force: bool = False, actor: str | None = None) -> DocumentReference:
    """Index a Markdown file as a document of a model.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file; a relative path is relative to the project root, not the cwd.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        force: Track without checking that the file round-trips under the model.
        actor: Optional caller label; accepted for compatibility, no longer recorded (the journal was retired on 2026-11-04).

    Returns:
        The tracked document.

    Raises:
        SLDBStoreError: When the model is not registered.
        SLDBValidationError: When the file does not round-trip, or when it carries
            headings the model does not declare, and `force` is False.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    doc_name = name or doc_path.stem
    text = read_source_text(doc_path)
    if not force:
        _refuse_unfit(registered.model_type, text, doc_name, location.store_path)
    check_entering_text(location.store_path, registered.model_type, registered.entry.name, doc_name, text, force)
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The path to track, refused before it is opened when it is a symlink or escapes the root
    (`source_read.refuse_unreadable`): resolving it first would track what it points to."""
    joined = root / Path(raw)
    refuse_unreadable(root, joined)
    return joined.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    declare_tracked(sp, root, registered.entry.name, project_relative(root, doc_path), doc_name)


def _refuse_unfit(model_type: type, text: str, doc_name: str, store_path: Path) -> None:
    """Refuse a text that does not round-trip, or carries noise or frontmatter the model does not declare."""
    _check_roundtrip(model_type, text)
    refuse_structural_noise(model_type, text, doc_name, Policy.of_store(store_path))
    refuse_undeclared_frontmatter(model_type, text, doc_name)


def _check_roundtrip(model_type: type, text: str) -> None:
    """Refuse a file that does not extract and re-render identically under the model."""
    valid, details = validate_model_input_roundtrip(model_type, text)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
