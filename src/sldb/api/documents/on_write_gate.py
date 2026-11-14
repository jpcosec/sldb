"""H4: a document that enters the store (`create_document`, `track_document_file`) passes the
`on_write` rules as a save would (rules.md §9.1): an `error` refuses it before anything is
written or tracked. There is no earlier index to read, so the subject is the document with its
model, its tags and the new payload, and no previous edges."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rules_on_write import check_on_write
from sldb.runtime.validation import extract_model_data


def check_entering(store_path: Path, model_type: type, model_name: str, doc_name: str, payload: dict[str, Any]) -> None:
    """Raise `SLDBRuleViolationError` when `payload` as `model_name:doc_name` breaks an `on_write` rule."""
    check_on_write(store_path, model_type, f"{model_name}:{doc_name}", payload)


def check_entering_text(store_path: Path, model_type: type, model_name: str, doc_name: str, text: str, force: bool = False) -> None:
    """The same, for a file's text: its payload is what the model extracts from it. A file the
    model cannot extract (tracked with `force`) has no payload to read and is not evaluated."""
    try:
        payload = extract_model_data(model_type, text)
    except Exception:  # noqa: BLE001 - pydantic or extractor errors alike
        if force:
            return
        raise
    check_entering(store_path, model_type, model_name, doc_name, payload)
