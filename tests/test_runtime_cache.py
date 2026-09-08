"""The runtime document cache: repeated loads share documents, a write to one document
re-extracts only that one, and a save that changes nothing leaves the file alone."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.cli import main as sldb_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_documents_index, load_models_index, load_store_index, save_documents_index
from sldb.store.query import load_runtime_documents
from sldb.store.runtime_cache import invalidate_runtime_cache

MODEL = "cachefix_models:NoteDoc"


def _world(tmp_path: Path) -> Path:
    (tmp_path / "cachefix_models.py").write_text(
        "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
        "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
        "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
    )
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(["models", "add", MODEL, "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)]) == 0
    for name in ("one", "two"):
        (tmp_path / f"{name}.md").write_text(f"# {name}\n\nbody of {name}\n")
        assert sldb_main(["docs", "track", str(tmp_path / f"{name}.md"), "--model", "NoteDoc", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)]) == 0
    return tmp_path


def test_repeated_loads_share_documents_and_a_write_reloads_one(tmp_path: Path):
    root = _world(tmp_path)
    invalidate_runtime_cache()
    first = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    second = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    assert [id(d) for d in first] == [id(d) for d in second]
    (root / "one.md").write_text("# one\n\nbody of one, changed\n")
    stale = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert stale["one"].payload["body"] == "body of one"   # the chain has not moved: an edit behind sldb's back waits for stores update
    assert sldb_main(["stores", "update", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    third = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    by_name = {d.name: d for d in third}
    assert by_name["one"].payload["body"] == "body of one, changed"
    assert id(by_name["two"]) == id({d.name: d for d in first}["two"])


def test_a_save_that_changes_nothing_leaves_the_file_alone(tmp_path: Path):
    root = _world(tmp_path)
    m = next(m for m in load_store_index(root / ".sldb").models if m.name == "NoteDoc")
    d_path = root / load_models_index(root / m.models_index).documents_index
    idx = load_documents_index(d_path)
    save_documents_index(d_path, idx)
    save_documents_index(d_path, idx)
    stamp = os.stat(d_path).st_mtime_ns
    save_documents_index(d_path, load_documents_index(d_path))
    assert os.stat(d_path).st_mtime_ns == stamp
