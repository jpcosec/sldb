"""Fill new model fields into existing documents when a draft is promoted.

Adding a field with a default to a model with tracked documents leaves those documents
without the field's section. `plan_backfill` finds them; `apply_backfill` re-renders each
one under the new contract and records its own journal entry. A new field without a
default cannot be backfilled, so the plan raises an error that says what to do.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sldb.api.documents.payload_diff import field_label
from sldb.api.journal import doc_address, doc_hashes, record
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store.facade import get_tracked_docs
from sldb.store.hashing import hash_fields, hash_text


@dataclass
class BackfillDoc:
    """One document a backfill promote would rewrite: what it had and what it becomes."""

    name: str
    path: Path
    previous: dict[str, Any]
    new: dict[str, Any]
    rendered: str
    hash_c_before: str | None
    hash_d_before: str | None


def plan_backfill(store: str | Path | None, model_name: str, old_type: type, new_type: type) -> list[BackfillDoc]:
    """Documents whose re-render under the new contract differs from what is on disk."""
    location = open_store(store)
    docs = get_tracked_docs(model_name, location.store_path, location.project_root)
    return [b for b in (_plan_document(location, model_name, old_type, new_type, name, path) for name, path in docs) if b]


def _plan_document(location, model_name: str, old_type: type, new_type: type, name: str, path_str: str) -> BackfillDoc | None:
    path = Path(path_str)
    text = path.read_text(encoding="utf-8")
    previous = extract_model_data(old_type, text)
    new = _fill_new_defaults(new_type, old_type, _extract(new_type, model_name, name, text))
    rendered = render_model_markdown(new_type, new)
    if rendered + "\n" == text:
        return None
    hc, hd = doc_hashes(location.store_path, model_name, name)
    return BackfillDoc(name, path, previous, new, rendered, hc, hd)


def apply_backfill(store: str | Path | None, model_name: str, new_type: type, plan: list[BackfillDoc], actor: str | None) -> int:
    """Rewrite each planned document and record its own journal entry; returns the count."""
    location = open_store(store)
    for doc in plan:
        text = doc.rendered + "\n"
        doc.path.write_text(text, encoding="utf-8")
        record(location.store_path, _entry(location.store_path, model_name, new_type, doc, text, actor))
    return len(plan)


def _entry(sp: Path, model_name: str, new_type: type, doc: BackfillDoc, text: str, actor: str | None) -> dict[str, Any]:
    return {"operation": "backfill_document", "address": doc_address(model_name, doc.name), "field": field_label(doc.previous, doc.new), "previous_value": doc.previous, "new_value": doc.new, "hash_c_before": doc.hash_c_before, "hash_c_after": hash_text(text), "hash_d_before": doc.hash_d_before, "hash_d_after": hash_fields(new_type, text), "actor": actor}


def _fill_new_defaults(new_type: type, old_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """Replace a new field's empty extraction with its declared default, when it has one."""
    for name in new_type.model_fields:
        if name in old_type.model_fields:
            continue
        field = new_type.model_fields[name]
        if not field.is_required():
            payload[name] = field.default
    return payload


def _extract(model_type: type, model_name: str, name: str, text: str) -> dict[str, Any]:
    try:
        return extract_model_data(model_type, text)
    except ValidationError as exc:
        missing = missing_fields(exc)
        raise SLDBValidationError(missing_message(model_name, name, missing), {"document": name, "missing": missing}) from exc


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
