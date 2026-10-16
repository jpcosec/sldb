"""A document whose field hashes name a field its model dropped is a contract move, not a data
mutation, and `stores update` re-extracts it.

Any write of another document of the model re-stamps the model's contract to the current
class; from then on the model looked unmoved, the untouched document failed as a
`data_mutation` blamed on a file nobody edited, and `stores update` trusted its unchanged text
and never fixed it (deskops, RitualDoc losing `routine`).
"""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api import add_model, create_document, init_store, resolve_model_ref, update_store_indexes
from sldb.store.diagnostics import diagnose_store
from sldb.store.io import invalidate_index_cache
from sldb.store.layout import project_root
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_field_drift_models"
_WITH = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """---
routine: ⸢rev•routine⸥
---

# ⸢rev•title⸥"""
    title: str = Field(description="Title.")
    routine: str = Field(default="", description="Dropped later.")
'''
_WITHOUT = _WITH.replace('    routine: str = Field(default="", description="Dropped later.")\n', "")


def _reload(models: Path, source: str) -> None:
    (models / f"{MODULE}.py").write_text(source, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_index_cache()
    invalidate_runtime_cache()


def test_a_dropped_field_is_a_contract_move_that_update_fixes(tmp_path):
    models, root = tmp_path / "models", tmp_path / "repo"
    models.mkdir(), root.mkdir()
    _reload(models, _WITH)
    sp = init_store(root).store_path
    add_model(sp, f"{MODULE}:NoteDoc", str(models))
    create_document(sp, "NoteDoc", root / "old.md", {"title": "Old", "routine": "r-1"}, "old", str(models))
    _reload(models, _WITHOUT)
    create_document(sp, "NoteDoc", root / "new.md", {"title": "New"}, "new", str(models))  # re-stamps the contract
    diagnosis = diagnose_store(sp, resolve_model_ref, project_root(sp), str(models))
    assert not diagnosis.is_valid and [m.name for m in diagnosis.moved_contracts] == ["NoteDoc"]
    assert not diagnosis.damaged_documents
    update_store_indexes(sp, str(models))
    assert diagnose_store(sp, resolve_model_ref, project_root(sp), str(models)).is_valid
