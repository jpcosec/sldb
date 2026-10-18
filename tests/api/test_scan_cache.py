"""The content scans of `stores check` are not repeated for a document whose text, model
contract and reader did not move (task: stores check escala mal con el inventario de
símbolos Python)."""

from __future__ import annotations

import sys

import pytest

from sldb import api
from sldb.api.documents import rewrite_loss as rewrite_module
from sldb.api.stores.scan_rewrite_loss import scan_rewrite_loss

MODULE = "sldb_scan_cache_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
'''


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Note", str(tmp_path))
    for name in ("a", "b"):
        api.create_document(sp, "Note", root / f"{name}.md", {"title": name, "what": "W."}, name, str(tmp_path))
    yield sp, root, str(tmp_path)
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


@pytest.fixture
def renders(monkeypatch):
    calls = []
    real = rewrite_module.rewrite_loss
    monkeypatch.setattr(rewrite_module, "rewrite_loss", lambda *a, **k: calls.append(1) or real(*a, **k))
    return calls


def test_a_second_pass_over_an_unchanged_store_renders_nothing(store, renders):
    sp, root, py = store
    scan_rewrite_loss(sp, root, py)
    first = len(renders)
    assert scan_rewrite_loss(sp, root, py) == [] and len(renders) == first == 2


def test_an_edited_document_is_scanned_again_and_its_finding_reported(store, renders):
    sp, root, py = store
    scan_rewrite_loss(sp, root, py)
    (root / "a.md").write_text("# a\n\nAdded by hand.\n\n## What\n\nW.\n", encoding="utf-8")
    found = scan_rewrite_loss(sp, root, py)
    assert len(renders) == 3 and [(f["document"], f["lost"]) for f in found] == [("a", ["Added by hand."])]
