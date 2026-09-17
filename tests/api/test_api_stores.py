"""`sldb.api` store operations: open, link, refresh indexes; and the `sldb.cli` bridges over them."""

from __future__ import annotations

import pytest

from sldb.api import link_store, open_store, update_store_indexes
from sldb.cli import main as cli_main
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index


def test_open_store_resolves_store_and_project_root(api_store):
    location = open_store(str(api_store.store))
    assert location.store_path == api_store.store.resolve()
    assert location.project_root == api_store.root.resolve()
    assert get_store_context(str(api_store.store)) == (location.store_path, location.project_root)


def test_open_store_without_store_outside_any_project_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    with pytest.raises(SLDBStoreError, match="init --path"):
        open_store(None)


def test_link_store_records_link_and_refuses_duplicates(api_store, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    assert cli_main(["stores", "init", "--path", str(other)]) == 0
    linked = link_store(api_store.store, other / ".sldb", "shared")
    assert (linked.name, linked.path) == ("shared", str((other / ".sldb").resolve()))
    assert [s.name for s in load_store_index(api_store.store).stores] == ["shared"]
    with pytest.raises(SLDBStoreError, match="already linked"):
        link_store(api_store.store, other / ".sldb", "shared")


def test_link_store_refuses_a_directory_without_store(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="No store at"):
        link_store(api_store.store, tmp_path / "nowhere" / ".sldb", "ghost")


def test_update_store_indexes_reports_a_complete_refresh(api_store):
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.complete
    assert report.store_path == api_store.store.resolve()
    assert report.semantic_index.docs_processed >= 0


def test_update_store_indexes_skips_a_missing_document(api_store):
    (api_store.root / "login.md").unlink()
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.skipped_documents == ["login"]
    assert not report.complete
    assert cli_main(["stores", "update", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]) == 1
