from pathlib import Path
from sldb.store.resolver import ancestor_stores, find_project_store, global_store_path, find_local_store
from sldb.store.layout import store_index_path


def test_global_store_path():
    assert global_store_path() == Path.home() / ".sldb"


def test_find_local_store_in_start_dir(tmp_path):
    store = tmp_path / ".sldb"
    store.mkdir()
    (store / "store_index.yaml").write_text("stores: []\nmodels: []\nhash_a: ''\n")
    assert find_local_store(tmp_path) == store


def test_find_local_store_in_parent(tmp_path):
    store = tmp_path / ".sldb"
    store.mkdir()
    (store / "store_index.yaml").write_text("stores: []\nmodels: []\nhash_a: ''\n")
    nested = tmp_path / "src" / "models"
    nested.mkdir(parents=True)
    assert find_local_store(nested) == store


def test_find_local_store_with_core_layout(tmp_path):
    store = tmp_path / ".sldb"
    store.mkdir()
    store_index_path(store).parent.mkdir(parents=True, exist_ok=True)
    store_index_path(store).write_text("stores: []\nmodels: []\nhash_a: ''\n")
    assert find_local_store(tmp_path) == store


def test_find_local_store_returns_none_when_missing(tmp_path):
    assert find_local_store(tmp_path) is None


def test_project_store_skips_home_global_store(tmp_path, monkeypatch):
    home = tmp_path / "home"
    project = home / "project"
    project.mkdir(parents=True)
    global_store = home / ".sldb"
    global_store.mkdir()
    (global_store / "store_index.yaml").write_text("stores: []\nmodels: []\nhash_a: ''\n")
    monkeypatch.setenv("HOME", str(home))
    assert find_project_store(project) is None
    assert ancestor_stores(project) == [global_store]


def test_project_store_prefers_nested_store_over_ancestor(tmp_path):
    parent = tmp_path / "parent"
    nested = parent / "child"
    nested.mkdir(parents=True)
    for root in (parent, nested):
        store = root / ".sldb"
        store.mkdir()
        (store / "store_index.yaml").write_text("stores: []\nmodels: []\nhash_a: ''\n")
    assert find_project_store(nested / "src") == nested / ".sldb"
