"""Start tracking an existing Markdown file as a document of a registered model."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.journal import doc_address, doc_hashes, record, store_hash
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.ops import track_document


def track_document_file(store: str | Path | None, model_name: str, path: str | Path, name: str | None = None, pythonpath: str | None = None, force: bool = False, actor: str | None = None) -> DocumentReference:
    """Index a Markdown file as a document of a model.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file; a relative path is relative to the project root, not the cwd.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        force: Track without checking that the file round-trips under the model.
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The tracked document.

    Raises:
        SLDBStoreError: When the model is not registered.
        SLDBValidationError: When the file does not round-trip and `force` is False.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    if not force:
        _check_roundtrip(registered.model_type, doc_path)
    doc_name = name or doc_path.stem
    _track_and_record(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath, actor)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    raw_path = Path(raw)
    return raw_path.resolve() if raw_path.is_absolute() else (root / raw_path).resolve()


def _track_and_record(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None, actor: str | None) -> None:
    before = store_hash(sp)
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    hash_c, hash_d = doc_hashes(sp, registered.entry.name, doc_name)
    record(sp, {"operation": "track_document_file", "address": doc_address(registered.entry.name, doc_name), "hash_c_after": hash_c, "hash_d_after": hash_d, "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})


def _check_roundtrip(model_type: type, doc_path: Path) -> None:
    """Refuse a file that does not extract and re-render identically under the model."""
    valid, details = validate_model_input_roundtrip(model_type, doc_path.read_text(encoding="utf-8"))
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
