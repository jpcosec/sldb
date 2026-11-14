"""The verdict of a tracked document its model rejects (inbox 3895e9f7, H1): `stores check` names
it as `store/doc-invalid` and goes on with the rest of the store, instead of leaving with the
model's ValidationError. Out of ``diagnostics.py`` so that module stays within the size the
clean-code rules allow."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.diagnostics_models.document_diagnosis import DocumentDiagnosis
from sldb.store.hashing import hash_fields_with_map

_SHOWN = 3  # errors named in the message; the count says how many there are


def fields_state(model_type: Any, text: str, doc, content_on_disk: str) -> tuple[str, dict[str, str], bool] | DocumentDiagnosis:
    """(fields hash on disk, per-field map, fields ok), or the `DOC_INVALID` verdict when the model
    rejects the text. Without the class, intact text stands for intact fields."""
    if model_type is None:
        return "", {}, content_on_disk == doc.source_hash
    try:
        fields_on_disk, map_on_disk = hash_fields_with_map(model_type, text)
    except ValidationError as exc:
        return invalid_diagnosis(doc, getattr(model_type, "__name__", "?"), exc, content_on_disk)
    return fields_on_disk, map_on_disk, fields_on_disk == doc.content_hash


def invalid_diagnosis(doc, model: str, exc: ValidationError, content_on_disk: str) -> DocumentDiagnosis:
    """The document as its model rejects it: text compared, fields not extractable."""
    content_ok = content_on_disk == doc.source_hash
    return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=content_ok, fields_ok=False, path_exists=True, note=DiagnosisNote.DOC_INVALID, content_on_disk=content_on_disk, content_in_index=doc.source_hash, fields_in_index=doc.content_hash, detail=invalid_message(model, doc.path, exc))


def invalid_message(model: str, path: str, exc: ValidationError) -> str:
    """'invalid: <Model> rejects <path>: <N> validation error(s); first: <loc>: <msg>', the first
    line of each of at most three errors, without pydantic's documentation URL."""
    errors = exc.errors(include_url=False)
    shown = "; ".join(f"{'.'.join(str(p) for p in e['loc']) or '<document>'}: {str(e['msg']).splitlines()[0]}" for e in errors[:_SHOWN])
    return f"invalid: {model} rejects {path}: {len(errors)} validation error(s); first: {shown}"
