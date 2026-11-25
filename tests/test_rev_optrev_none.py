"""A rev marker whose value is None renders `null` and extracts back as None;
an optrev field that is None can be set again with `fields update`."""

from __future__ import annotations

import sys
from typing import Optional

import pytest
from pydantic import Field

from sldb import StructuredNLDoc, api
from sldb.cli import main as cli_main
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_rev_optrev_none_models"
_MODEL = '''from typing import Optional
from pydantic import Field
from sldb import StructuredNLDoc


class NoneDoc(StructuredNLDoc):
    __template__ = """---
nota: ⸢optrev•nota⸥
---

# ⸢rev•title⸥

owner: ⸢rev•owner⸥
"""
    title: str = Field(description="Title.")
    owner: Optional[str] = Field(default=None, description="Owner.")
    nota: Optional[str] = Field(default=None, description="Note.")
'''


class NoneDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

owner: ⸢rev•owner⸥
"""
    title: str = Field(description="Title.")
    owner: Optional[str] = Field(default=None, description="Owner.")


def test_rev_none_renders_null_and_extracts_none():
    md = render_model_markdown(NoneDoc, {"title": "T", "owner": None})
    assert "⸢" not in md
    assert "owner: null" in md
    assert extract_model_data(NoneDoc, md).get("owner") is None


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


def test_optrev_none_accepts_fields_update(store):
    tmp, py = store
    (tmp / f"{MODULE}.py").write_text(_MODEL, encoding="utf-8")
    root = tmp / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:NoneDoc", py)
    api.create_document(sp, "NoneDoc", root / "a.md", {"title": "A"}, "a", py)
    assert "nota" not in (root / "a.md").read_text(encoding="utf-8")
    code = cli_main(["fields", "update", "docs/a/nota", "x", "--string", "--store", str(sp), "--pythonpath", py])
    assert code == 0
    assert "nota: x" in (root / "a.md").read_text(encoding="utf-8")
