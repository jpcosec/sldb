"""A data mutation over untouched text points to `models update`, not to `stores update`.

After the extraction fixes of 2026-10-18 four documents of sldb's own store extracted more;
`stores check` said "`stores update` accepts it", but `stores update` trusts text that did not
move and changed nothing. Only `models update <Model>` re-extracts them.
"""

from __future__ import annotations

from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.diagnostics_models.document_diagnosis import DocumentDiagnosis


def _doc(content_ok: bool) -> DocumentDiagnosis:
    return DocumentDiagnosis(name="d", path="d.md", content_ok=content_ok, fields_ok=False, path_exists=True, note=DiagnosisNote.DATA_MUTATION)


def test_untouched_text_is_a_reread_that_needs_no_decision():
    doc = _doc(content_ok=True)
    assert "models update" in doc.remedy() and "models update" in doc.explain()
    assert not doc.needs_decision


def test_an_edited_file_still_needs_a_human():
    doc = _doc(content_ok=False)
    assert doc.needs_decision and "decide first" in doc.remedy()
