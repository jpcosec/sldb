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
    assert report == {"ok": True, "integrity_exit": 0, "undeclared": [], "differences": []}
    assert yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))["include"]
