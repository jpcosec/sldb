"""Check a loaded model contract against the documents a store tracks for that model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_drafts.draft_contract import validate_template_contract
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelEditError, SLDBModelError, SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.facade import get_tracked_docs
from sldb.store.io import load_models_index, load_store_index


def check_documents(store: str | Path | None, model_name: str, model_type: Any) -> list[DraftDocumentCheck]:
    """Check the template contract, then round-trip every tracked document of the model.

    The broad catch translates whatever a broken draft raises while being exercised
    (its class body, template parsing, extraction) into one domain error, chained.

    Raises:
        SLDBModelEditError: When the contract is inconsistent or the draft fails unexpectedly.
        SLDBValidationError: When a tracked document does not round-trip.
    """
    try:
        validate_template_contract(model_type)
        location = open_store(store)
        return [_check_document(model_name, name, Path(path), model_type) for name, path in get_tracked_docs(model_name, location.store_path, location.project_root)]
    except (SLDBValidationError, SLDBModelError):
        raise
    except Exception as exc:
        raise SLDBModelEditError(f"Draft for '{model_name}' is invalid: {exc}") from exc


def _check_document(model_name: str, name: str, path: Path, model_type: Any) -> DraftDocumentCheck:
    """Round-trip one document; a document that does not round-trip stops the validation."""
    valid, details = validate_model_input_roundtrip(model_type, path.read_text(encoding="utf-8"))
    if not valid:
        raise SLDBValidationError(f"Draft for '{model_name}' failed validation on '{name}'.", details)
    return DraftDocumentCheck(name=name, path=path, valid=valid)


def current_version(store: str | Path | None, model_name: str) -> int:
    """The contract version the store's models index records for a model (1 when unregistered)."""
    location = open_store(store)
    entry = next((m for m in load_store_index(location.store_path).models if m.name == model_name), None)
    return load_models_index(location.project_root / entry.models_index).version if entry else 1
