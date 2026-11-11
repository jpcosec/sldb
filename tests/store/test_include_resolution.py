"""A file in a parent model's glob and in a child model's `paths` is tracked once, under the
child (task.debug dbltrack). A clean build tracked it under both, and `Parent:name` was ambiguous."""
from __future__ import annotations

import sys

import pytest

from sldb.api import build_store
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.resolve_indexed_document import resolve_indexed_document
from sldb.api.stores.store_declaration import StoreDeclaration, load_declaration, save_declaration
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.cli import main as cli_main
from sldb.store.io import invalidate_index_cache

MODELS = """from pydantic import Field
from sldb import StructuredNLDoc

class ParentDoc(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')

class ChildDoc(ParentDoc):
    pass

class OtherDoc(StructuredNLDoc):
    __template__ = '# ⸢rev•title⸥'
    title: str = Field(description='Title')
"""
GLOB = {"model": "ParentDoc", "glob": "docs/*.md"}


@pytest.fixture
def project(tmp_path):
    (tmp_path / "famdocs").mkdir()
    (tmp_path / "famdocs" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "famdocs" / "models.py").write_text(MODELS, encoding="utf-8")
    (tmp_path / "docs").mkdir()
    for stem in ("a", "b", "c"):
        (tmp_path / "docs" / f"{stem}.md").write_text(f"# {stem}\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    yield tmp_path
    sys.path.remove(str(tmp_path))
    for name in [m for m in sys.modules if m == "famdocs" or m.startswith("famdocs.")]:
        del sys.modules[name]


def _declare(root, *include):
    models = [{"name": n, "model_ref": f"famdocs.models:{n}", "path": "famdocs/models.py"} for n in ("ParentDoc", "ChildDoc", "OtherDoc")]
    (root / ".sldb").mkdir(exist_ok=True)
    save_declaration(root / ".sldb", StoreDeclaration(models=models, include=list(include)))
    invalidate_index_cache()
    return root / ".sldb"


def test_a_clean_build_tracks_the_file_once_under_the_child(project):
    store = _declare(project, GLOB, {"model": "ChildDoc", "paths": ["docs/a.md", "docs/b.md"]})
    report = build_store(store)
    assert report["include_conflicts"] == [] and report["undeclared"] == []
    assert tracked_rows(store, project) == [("ChildDoc", "docs/a.md", "a"), ("ChildDoc", "docs/b.md", "b"), ("ParentDoc", "docs/c.md", "c")]
    assert resolve_indexed_document(store, "ParentDoc", "a") == {"name": "a", "model": "ChildDoc", "path": "docs/a.md"}
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_the_same_model_in_a_glob_and_in_paths_is_one_row_without_conflict(project):
    store = _declare(project, GLOB, {"model": "ParentDoc", "paths": [{"path": "docs/a.md", "name": "alpha"}]})
    assert build_store(store)["include_conflicts"] == []
    assert tracked_rows(store, project) == [("ParentDoc", "docs/a.md", "alpha"), ("ParentDoc", "docs/b.md", "b"), ("ParentDoc", "docs/c.md", "c")]


def test_a_store_already_tracking_twice_is_fixed_by_update_and_build_idempotently(project):
    store = _declare(project, GLOB)
    build_store(store)
    assert cli_main(["docs", "track", str(project / "docs" / "a.md"), "--model", "ChildDoc", "--store", str(store), "--pythonpath", str(project)]) == 0
    declared = (store / "store.yaml").read_text(encoding="utf-8")
    assert load_declaration(store).include == [GLOB, {"model": "ChildDoc", "paths": ["docs/a.md"]}]
    assert {r[0] for r in tracked_rows(store, project) if r[1] == "docs/a.md"} == {"ParentDoc", "ChildDoc"}
    update_store_indexes(store)
    rows = tracked_rows(store, project)
    assert [r for r in rows if r[1] == "docs/a.md"] == [("ChildDoc", "docs/a.md", "a")] and len(rows) == 3
    assert build_store(store)["tracked"] == [] and update_store_indexes(store).complete
    assert tracked_rows(store, project) == rows and (store / "store.yaml").read_text(encoding="utf-8") == declared
    assert (project / "docs" / "a.md").read_text(encoding="utf-8") == "# a\n"


def test_models_with_no_descent_between_them_are_an_include_conflict(project, capsys):
    store = _declare(project, GLOB, {"model": "OtherDoc", "paths": ["docs/a.md"]})
    report = build_store(store)
    assert [(c["level"], c["code"], c["subject"]) for c in report["include_conflicts"]] == [("error", "store/include-conflict", "docs/a.md")]
    assert "OtherDoc" in report["include_conflicts"][0]["what"] and report["undeclared"] == []
    assert [r[1] for r in tracked_rows(store, project)] == ["docs/b.md", "docs/c.md"]
    capsys.readouterr()
    assert cli_main(["stores", "build", "--store", str(store)]) == 1
    assert "error: [store/include-conflict] docs/a.md" in capsys.readouterr().out
    assert cli_main(["stores", "check", "--store", str(store)]) == 1
    assert "store/include-conflict" in capsys.readouterr().out


def test_two_paths_rules_of_parent_and_child_are_a_conflict_too(project):
    store = _declare(project, {"model": "ParentDoc", "paths": ["docs/a.md"]}, {"model": "ChildDoc", "paths": ["docs/a.md"]})
    assert [c["subject"] for c in build_store(store)["include_conflicts"]] == ["docs/a.md"]
