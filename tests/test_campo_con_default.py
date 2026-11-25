"""A field added later with a default does not invalidate the documents written before it:
a document without the key takes the model's default on extraction and stays valid."""

from __future__ import annotations

import sys

import pytest

from sldb import api
from sldb.runtime.validation import extract_model_data
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_campo_con_default_models"
_BEFORE = '''from pydantic import Field
from sldb import StructuredNLDoc


class Asistente(StructuredNLDoc):
    __template__ = """---
nombre: ⸢rev•nombre⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    nombre: str = Field(description="Name.")
'''
_AFTER = _BEFORE.replace(
    "---\n\n# ⸢rev•title⸥",
    "espera_segundos: ⸢rev•espera_segundos⸥\n---\n\n# ⸢rev•title⸥",
).replace(
    '    nombre: str = Field(description="Name.")\n',
    '    nombre: str = Field(description="Name.")\n    espera_segundos: int = Field(default=4, description="Wait.")\n',
)


@pytest.fixture
def store(tmp_path):
    py = str(tmp_path)
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()
    sys.path.insert(0, py)
    try:
        yield tmp_path, py
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)
        invalidate_runtime_cache()


def test_a_document_without_the_new_field_takes_the_default_and_stays_valid(store):
    tmp, py = store
    (tmp / f"{MODULE}.py").write_text(_BEFORE, encoding="utf-8")
    root = tmp / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Asistente", py)
    api.create_document(sp, "Asistente", root / "a.md", {"title": "A", "nombre": "x"}, "a", py)

    (tmp / f"{MODULE}.py").write_text(_AFTER, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()

    report = api.check_store(sp, root, py)
    assert [e for e in report["errors"] + report["alerts"] if e["code"] == "store/doc-invalid"] == []
    model = getattr(__import__(MODULE), "Asistente")
    got = extract_model_data(model, (root / "a.md").read_text(encoding="utf-8"))
    assert got["espera_segundos"] == 4
