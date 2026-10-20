"""A model that cannot be imported is named, not blamed on its documents.

Without the class the fields cannot be re-extracted, and the check used to read that as a data
mutation on every document ("decide first", restore the file) — in a clean clone without the
model's package, in a consumer's CI with another `sldb` first on PATH. Intact text now stands
for intact fields and the model is reported unresolved; changed text still fails.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api import add_model, init_store, resolve_model_ref, track_document_file
from sldb.runtime.validation import render_model_markdown
from sldb.store.diagnostics import diagnose_store
from sldb.store.io import invalidate_index_cache
from sldb.store.layout import project_root
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_unresolved_check_models"
_NOTE = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥""".strip()
    title: str = Field(description="Note title.")
'''


def _store_without_its_model(tmp_path: Path) -> Path:
    models = tmp_path / "models"
    models.mkdir()
    (models / f"{MODULE}.py").write_text(_NOTE, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    sp = init_store(root).store_path
    add_model(sp, f"{MODULE}:NoteDoc", str(models))
    model_type = resolve_model_ref(f"{MODULE}:NoteDoc", str(models))
    (root / "note.md").write_text(render_model_markdown(model_type, {"title": "A note"}) + "\n", encoding="utf-8")
    track_document_file(sp, "NoteDoc", root / "note.md", "note", str(models))
    (models / f"{MODULE}.py").unlink()
    sys.modules.pop(MODULE, None)
    invalidate_index_cache()
    invalidate_runtime_cache()
    return sp


def test_an_unimportable_model_is_an_error_and_is_named(tmp_path):
    """A model that does not import is an error (anchoring.md §4): its fields went unchecked."""
    from sldb.api.stores.store_findings import diagnosis_findings

    sp = _store_without_its_model(tmp_path)
    diagnosis = diagnose_store(sp, resolve_model_ref, project_root(sp))
    assert not diagnosis.is_valid
    assert not diagnosis.models[0].resolved
    assert [(f.level, f.code, f.subject) for f in diagnosis_findings(diagnosis)] == [("error", "store/model-unresolved", "NoteDoc")]


def test_an_unimportable_model_does_not_excuse_changed_text(tmp_path):
    sp = _store_without_its_model(tmp_path)
    (project_root(sp) / "note.md").write_text("# Edited by hand\n", encoding="utf-8")
    diagnosis = diagnose_store(sp, resolve_model_ref, project_root(sp))
    assert not diagnosis.is_valid
    from sldb.api.stores.store_findings import diagnosis_findings

    assert "store/data-mutation" in [f.code for f in diagnosis_findings(diagnosis)], "the changed text is reported too"
