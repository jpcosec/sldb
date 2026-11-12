"""A store of three memos, two of them (`a`, `b`) edited by hand into a status their model
rejects: the reproduction of inbox 3895e9f7 (H1-H3), shared by its tests. The model declares
a reference, so rebuilding its edges reads each document's payload (where H2 fell)."""

from __future__ import annotations

import sys

import pytest

from sldb import api
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_doc_invalid_check_models"
_MODELS = '''from pydantic import Field, field_validator
from sldb import StructuredNLDoc


class Memo(StructuredNLDoc):
    __references__ = ["about"]
    __template__ = """---
status: ⸢rev•status⸥
about: ⸢rev•about⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    about: str = Field(description="The memo it answers: read for its declared edge.")

    @field_validator("status")
    @classmethod
    def _known(cls, value):
        if value == "bad":
            raise ValueError("status bad is not a status")
        return value
'''


@pytest.fixture
def store_with_invalid(tmp_path):
    """Three memos; `a` and `b` then edited by hand into a status the model rejects."""
    py = str(tmp_path)
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()
    sys.path.insert(0, py)
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Memo", py)
        for name in ("a", "b", "c"):
            api.create_document(sp, "Memo", root / f"{name}.md", {"title": name, "status": "open", "about": "c"}, name, py)
        for name in ("a", "b"):
            path = root / f"{name}.md"
            path.write_text(path.read_text(encoding="utf-8").replace("status: open", "status: bad"), encoding="utf-8")
        yield root, sp, py
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)
