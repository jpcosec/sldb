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
    assert diagnosis.is_valid and [m.name for m in diagnosis.moved_contracts] == ["NoteDoc"], "a moved contract is an alert"
    assert not diagnosis.damaged_documents
    update_store_indexes(sp, str(models))
    assert diagnose_store(sp, resolve_model_ref, project_root(sp), str(models)).is_valid


_EXTRA = '''from pydantic import ConfigDict, Field, model_validator
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    """The shape of deskops' TaskDoc: the frontmatter is one dict whose keys become extras."""
    model_config = ConfigDict(extra="allow")
    __template__ = """---
⸢rev,dict•frontmatter⸥
---

# ⸢rev•title⸥"""
    title: str = Field(description="Title.")
    frontmatter: dict | None = Field(default=None, description="Metadata.", exclude=True)

    @model_validator(mode="before")
    @classmethod
    def _merge_frontmatter(cls, data):
        if isinstance(data, dict) and isinstance(data.get("frontmatter"), dict):
            for key, value in data.pop("frontmatter").items():
                data.setdefault(key, value)
        return data

    def render_payload(self, ref_root=None):
        data = super().render_payload(ref_root)
        data["frontmatter"] = {k: v for k, v in data.items() if k != "title"}
        return data
'''


def test_an_extra_key_the_class_still_yields_is_not_another_contract(tmp_path):
    """`extra="allow"` promotes an undeclared frontmatter key into the payload, so its field
    hash comes from the current contract. Counting it as a dropped field made `stores check`
    report a contract move that `stores update` could never clear (graph_ui, TaskDoc)."""
    from sldb.api import track_document_file
    from sldb.store.io import load_documents_index, load_models_index, load_store_index

    models, root = tmp_path / "models", tmp_path / "repo"
    models.mkdir(), root.mkdir()
    _reload(models, _EXTRA)
    sp = init_store(root).store_path
    add_model(sp, f"{MODULE}:NoteDoc", str(models))
    (root / "task.md").write_text("---\npriority: p0\n---\n\n# A task\n", encoding="utf-8")
    track_document_file(sp, "NoteDoc", root / "task.md", "task", str(models))
    m_idx = load_models_index(root / load_store_index(sp).models[0].models_index)
    assert "priority" in load_documents_index(root / m_idx.documents_index).documents[0].field_hashes

    diagnosis = diagnose_store(sp, resolve_model_ref, project_root(sp), str(models))
    assert diagnosis.is_valid and not diagnosis.moved_contracts
