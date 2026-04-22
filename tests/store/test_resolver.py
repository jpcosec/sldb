from pathlib import Path
from sldb.store.resolver import global_store_path, find_local_store


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


def test_find_local_store_returns_none_when_missing(tmp_path):
    assert find_local_store(tmp_path) is None
