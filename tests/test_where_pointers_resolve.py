"""anchors_resolve: which documents cover a file or symbol, which code a document or tag covers."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

import sldb.api as api
from sldb.api.anchors import record_anchor, write_anchor
from sldb.code.runtime import available
from sldb.core.exceptions import SLDBStoreError
from sldb.mcp.read import ReadTools
from sldb.store.io import load_semantic_dag, save_semantic_dag

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

MODULE = "pointers_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "---\\ntags: ⸢optrev,list•tags⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    tags: list[str] = Field(default_factory=list, description="Pointers to categories.")
'''
CODE = 'def free(a):\n    """Free."""\n    return a\n\n\ndef other(b):\n    """Other."""\n    return b\n'


@pytest.fixture
def world(tmp_path):
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "repo", str(tmp_path)
    (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    api.add_model(store, f"{MODULE}:Note", py)
    block = {**record_anchor(root, "code:src/x.py::free"), "tags": ["layer.interface.panel"]}
    write_anchor(store, py, root / "anchors" / "free.md", block, "free returns a", "free")
    api.create_document(store, "Note", root / "parent.md", {"title": "P", "tags": ["layer.interface"]}, "parent", py)
    api.create_document(store, "Note", root / "stray.md", {"title": "S", "tags": ["layer.other"]}, "stray", py)
    api.create_document(store, "Note", root / "ghost.md", {"title": "G", "tags": ["layer.ghost"]}, "ghost", py)
    yield store, py
    sys.modules.pop(MODULE, None)


def test_a_file_is_covered_directly_and_through_a_parent_tag(world):
    store, py = world
    got = api.anchors_resolve(store, target="src/x.py", pythonpath=py)
    assert got["documents"] == [{"doc": "CodeAnchorDoc:free", "via": "direct"}, {"doc": "Note:parent", "via": "tag:layer.interface"}]
    assert api.anchors_resolve(store, target="code:src/x.py::free", pythonpath=py)["documents"] == got["documents"]
    assert api.anchors_resolve(store, target="src/x.py::other", pythonpath=py)["documents"] == []


def test_a_tag_reaches_the_documents_below_it_and_their_code(world):
    store, py = world
    got = api.anchors_resolve(store, tag="layer.interface", pythonpath=py)
    assert {"doc": "Note:parent", "via": "tag:layer.interface"} in got["documents"]
    assert got["code"] == [{"path": "src/x.py", "symbol": "free", "via": "tag:layer.interface"}]
    assert api.anchors_resolve(store, document="Note:parent", pythonpath=py)["code"] == got["code"]
    assert api.anchors_resolve(store, document="CodeAnchorDoc:free", pythonpath=py)["code"] == [{"path": "src/x.py", "symbol": "free", "via": "direct"}]


def test_a_pointer_to_a_missing_tag_is_reported_not_raised(world):
    store, py = world
    dag = load_semantic_dag(store)
    dag.nodes = [n for n in dag.nodes if n.id != "layer.ghost"]
    save_semantic_dag(store, dag)
    assert {"tag": "layer.ghost", "doc": "Note:ghost"} in api.anchors_resolve(store, target="src/x.py", pythonpath=py)["unresolved"]
    assert api.anchors_resolve(store, tag="nope", pythonpath=py)["unresolved"] == [{"tag": "layer.ghost", "doc": "Note:ghost"}, {"tag": "nope", "doc": ""}]


def test_exactly_one_question_and_nothing_is_written(world):
    store, py = world
    with pytest.raises(SLDBStoreError):
        api.anchors_resolve(store, target="src/x.py", tag="a", pythonpath=py)
    with pytest.raises(SLDBStoreError):
        api.anchors_resolve(store, document="Note:nobody", pythonpath=py)
    before = {p: p.read_bytes() for p in store.parent.rglob("*") if p.is_file()}
    api.anchors_resolve(store, target="src/x.py", pythonpath=py)
    assert before == {p: p.read_bytes() for p in store.parent.rglob("*") if p.is_file()}


def test_the_mcp_tool_has_the_same_name_and_answer(world):
    store, py = world
    assert ReadTools(store).anchors_resolve(target="src/x.py")["documents"] == api.anchors_resolve(store, target="src/x.py", pythonpath=py)["documents"]
