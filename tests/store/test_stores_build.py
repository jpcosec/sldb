"""`stores declare` / `stores build`: the derived store comes back from what the store declares."""
from __future__ import annotations

import shutil
import subprocess
import sys

import pytest
import yaml

from sldb.api.stores.apply_declaration import undeclared
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.cli import main as cli_main
from sldb.cli.commands.stores_build import build_store
from sldb.cli.commands.stores_build_check import check_build
from sldb.store.io import invalidate_index_cache

from .test_semantic_export import _build_tracked_store


@pytest.fixture(autouse=True)
def _forget_the_tmp_model_package():
    yield
    for name in [m for m in sys.modules if m == "tmpdocs" or m.startswith("tmpdocs.")]:
        del sys.modules[name]


def _declared(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    save_declaration(store, declare_store(store, root))
    return store, root


def test_the_declaration_names_what_is_tracked_and_nothing_else(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    assert [m["name"] for m in declaration.models] == ["TaskDoc"]
    assert declaration.include == [{"model": "TaskDoc", "paths": ["task.md"]}]
    assert undeclared(store, root, declaration) == []


def test_a_store_rebuilt_from_its_declaration_tracks_the_same(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    before = tracked_rows(store, root)
    for derived in ("core", "runtime"):
        shutil.rmtree(store / derived, ignore_errors=True)
    invalidate_index_cache()
    report = build_store(store, root)
    assert report["models"] == ["TaskDoc"] and report["tracked"] == ["task.md"]
    assert tracked_rows(store, root) == before
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_building_a_current_store_changes_nothing(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    report = build_store(store, root)
    assert report["links"] == report["models"] == report["tracked"] == report["undeclared"] == []
    assert report["predicates_changed"] is False


def test_a_tracked_document_no_rule_names_is_reported(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    declaration.include = []
    assert undeclared(store, root, declaration) == ["task.md"]


def test_the_check_rebuilds_a_scratch_copy_and_compares(tmp_path, capsys):
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    (root / ".gitignore").write_text(".sldb/runtime/\n.sldb/core/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report == {"ok": True, "integrity_exit": 0, "undeclared": [], "missing": [], "differences": []}
    assert yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))["include"]


def test_build_finds_a_store_that_is_only_declared(tmp_path, capsys, monkeypatch):
    """A fresh clone has `.sldb/store.yaml` and no index: the usual discovery, which looks for
    the index, missed it and fell back to the global store."""
    store, root = _declared(tmp_path, capsys)
    for derived in ("core", "runtime"):
        shutil.rmtree(store / derived, ignore_errors=True)
    invalidate_index_cache()
    monkeypatch.chdir(root)
    assert cli_main(["stores", "build"]) == 0
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_a_model_outside_the_project_is_declared_by_reference_only(tmp_path, capsys):
    """deskops and spec2viz register sldb's relation models from the installed package: their
    absolute path would pin the declaration to one checkout."""
    from sldb.api import add_model

    store, root = _build_tracked_store(tmp_path, capsys)
    add_model(store, "sldb.models.relation_doc:RelationDoc")
    models = {m["name"]: m for m in declare_store(store, root).models}
    assert models["RelationDoc"] == {"name": "RelationDoc", "model_ref": "sldb.models.relation_doc:RelationDoc"}
    assert models["TaskDoc"]["path"] == "tmpdocs/models.py"


def test_a_folder_with_one_tracked_file_is_listed_not_globbed(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    (root / "boards").mkdir()
    (root / "boards" / "board.md").write_text("# Board\n\n## Overview\n\nBody\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "boards" / "board.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    rules = [r for r in declare_store(store, root).include if "boards/board.md" in str(r)]
    assert rules == [{"model": "TaskDoc", "paths": ["boards/board.md"]}]


def test_untracking_a_document_takes_it_out_of_the_declaration(tmp_path, capsys):
    """deskops retire untracks a note; the declaration kept listing it, so a clean clone
    could not rebuild (CI run 39274588896)."""
    store, root = _declared(tmp_path, capsys)
    assert cli_main(["docs", "untrack", "task", "--store", str(store)]) == 0
    assert load_declaration(store).include == []


def test_tracking_a_document_no_rule_covers_adds_it_to_the_declaration(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    (root / "second.md").write_text("# Beta\n\n## Overview\n\nMore\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "second.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert load_declaration(store).include == [{"model": "TaskDoc", "paths": ["task.md", "second.md"]}]
    assert undeclared(store, root, load_declaration(store)) == []


def test_a_declared_file_that_is_gone_is_reported_not_raised(tmp_path, capsys):
    """The clean-clone failure: the declaration names a file git no longer has."""
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    declaration = load_declaration(store)
    declaration.include[0]["paths"].append("gone.md")
    save_declaration(store, declaration)
    (root / ".gitignore").write_text(".sldb/runtime/\n.sldb/core/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report["ok"] is False and report["missing"] == ["gone.md"]
    assert report["integrity_exit"] == 0
