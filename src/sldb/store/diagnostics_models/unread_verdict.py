"""The verdict of a tracked document that ``stores check`` does not read (SEGURIDAD live_stale,
inbox 9c9dac6b): its path resolves outside the project root or is a symlink
(``source_read.unreadable_reason``), or the file is missing. Out of ``diagnostics.py`` so that
module stays within the size the clean-code rules allow."""

from __future__ import annotations

from pathlib import Path

from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.diagnostics_models.document_diagnosis import DocumentDiagnosis
from sldb.store.source_read import OUTSIDE_ROOT, unreadable_reason


def unread_diagnosis(doc, root: Path, doc_path: Path) -> DocumentDiagnosis | None:
    """The verdict of a document that is not read; None when it may be read."""
    if (reason := unreadable_reason(root, doc_path)) is not None:
        note = DiagnosisNote.PATH_OUTSIDE_ROOT if reason == OUTSIDE_ROOT else DiagnosisNote.SYMLINK_NOT_READ
        return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=False, fields_ok=False, path_exists=True, note=note, content_in_index=doc.source_hash, fields_in_index=doc.content_hash)
    if not doc_path.exists():
        return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=False, fields_ok=False, path_exists=False, note=DiagnosisNote.MISSING, content_in_index=doc.source_hash, fields_in_index=doc.content_hash)
    return None
