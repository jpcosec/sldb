"""Check every document under a draft and plan the backfill of new fields.

A document written before a field existed lacks the field's section. `check_and_plan`
extracts it under the old contract, adds the new fields' defaults, validates that the
filled payload round-trips under the new contract, and reports which documents a backfill
would rewrite. `apply_backfill` re-renders each one, stamped with the actor.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sldb.api.model_drafts.draft_contract import validate_template_contract
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelEditError, SLDBModelError, SLDBValidationError
from sldb.api.documents.provenance_stamp import stamped_file
from sldb.runtime.validation import extract_model_data, render_model_markdown, validate_model_data_roundtrip
from sldb.store.facade import get_tracked_docs
from sldb.store.source_guard import aggregate_text, write_source_text


@dataclass
class BackfillDoc:
    """One document a backfill promote would rewrite: what it had and what it becomes."""

    name: str
    path: Path
    previous: dict[str, Any]
    new: dict[str, Any]
    rendered: str
    needs_write: bool = True


def check_and_plan(store: str | Path | None, model_name: str, old_type: type, new_type: type) -> tuple[list[DraftDocumentCheck], list[BackfillDoc]]:
    """Check every document under the new contract and return the backfill plan."""
    validate_template_contract(new_type)
    location = open_store(store)
    docs = get_tracked_docs(model_name, location.store_path, location.project_root)
    prepared = _prepare_all(location, model_name, old_type, new_type, docs)
    checks = [DraftDocumentCheck(name=d.name, path=d.path, valid=True) for d in prepared]
    return checks, [d for d in prepared if d.needs_write]


def _prepare_all(location, model_name: str, old_type: type, new_type: type, docs: list[tuple[str, str]]) -> list[BackfillDoc]:
    try:
        return [d for name, path in docs if (d := _prepare(location, model_name, old_type, new_type, name, path)) is not None]
    except (SLDBValidationError, SLDBModelError):
        raise
    except Exception as exc:  # noqa: BLE001 - a broken draft raises whatever it raises
        raise SLDBModelEditError(f"Draft for '{model_name}' is invalid: {exc}") from exc


def apply_backfill(store: str | Path | None, model_name: str, new_type: type, plan: list[BackfillDoc], actor: str | None) -> int:
    """Rewrite each planned document, stamped with the actor; returns the count."""
    for doc in plan:
        write_source_text(doc.path, stamped_file(doc.path, doc.rendered + "\n", new_type, "backfill_document", actor))
    return len(plan)


def _prepare(location, model_name: str, old_type: type, new_type: type, name: str, path_str: str) -> BackfillDoc | None:
    """The backfill of one document; None (warned with its finding) when the read guard refuses its path."""
    if (text := aggregate_text(location.project_root, path := Path(path_str), f"{model_name}:{name}")) is None:
        return None
    previous = extract_model_data(old_type, text)
    new = _add_new_defaults(new_type, old_type, previous, model_name, name)
    _check_roundtrip(new_type, model_name, name, new)
    rendered = render_model_markdown(new_type, new, location.project_root)
    comps_changed = getattr(old_type, "__compositions__", {}) != getattr(new_type, "__compositions__", {})
    tpl_changed = getattr(old_type, "__template__", "") != getattr(new_type, "__template__", "")
    needs_write = (rendered + "\n" != text) or comps_changed or tpl_changed
    return BackfillDoc(name, path, previous, new, rendered, needs_write)


def _add_new_defaults(new_type: type, old_type: type, payload: dict[str, Any], model_name: str, name: str) -> dict[str, Any]:
    filled = dict(payload)
    for field_name in new_type.model_fields:
        if field_name in old_type.model_fields:
            continue
        field = new_type.model_fields[field_name]
        if field.is_required():
            raise SLDBValidationError(missing_message(model_name, name, [field_name]), {"document": name, "missing": [field_name]})
        filled[field_name] = field.default
    return filled


def _check_roundtrip(new_type: type, model_name: str, name: str, payload: dict[str, Any]) -> None:
    valid, details = validate_model_data_roundtrip(new_type, payload)
    if not valid:
        raise SLDBValidationError(f"Draft for '{model_name}' failed validation on '{name}'.", details)


def missing_fields(exc: ValidationError) -> list[str]:
    """The field names a pydantic ValidationError reports as missing."""
    return [str(e["loc"][0]) for e in exc.errors() if e.get("type") == "missing"]


def missing_message(model_name: str, name: str, missing: list[str]) -> str:
    """An actionable explanation of why a document lacks a required field."""
    fields = ", ".join(repr(f) for f in missing)
    return (
        f"Draft for '{model_name}' breaks '{name}': it lacks required field(s) {fields}, "
        "which have no default. Give each new field a default (so promote backfill can fill "
        "existing documents) or declare it optional (e.g. 'str | None'), then retry."
    )
