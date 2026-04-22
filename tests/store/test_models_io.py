import pytest
from pathlib import Path
from sldb.store.models import (
    StoreEntry, ModelEntry, StoreIndex,
    ModelsIndex, DocumentEntry, DocumentsIndex,
)
from sldb.store.io import (
    load_store_index, save_store_index,
    load_models_index, save_models_index,
    load_documents_index, save_documents_index,
)


def test_store_index_roundtrip(tmp_path):
    index = StoreIndex(
        stores=[StoreEntry(name="shared", path="~/.sldb")],
        models=[ModelEntry(name="Book", model_ref="myapp.models:Book", path="src/models/book.py", models_index=".sldb/models/Book.yaml")],
        hash_a="abc123",
    )
    save_store_index(tmp_path, index)
    assert load_store_index(tmp_path) == index


def test_store_index_empty_defaults(tmp_path):
    save_store_index(tmp_path, StoreIndex())
    loaded = load_store_index(tmp_path)
    assert loaded.stores == []
    assert loaded.models == []
    assert loaded.hash_a == ""


def test_models_index_roundtrip(tmp_path):
    index = ModelsIndex(
        name="Dictionary", model_ref="myapp.models:Dictionary",
        path="src/models/dictionary.py",
        documents_index=".sldb/documents/Dictionary.yaml",
        hash_b="def456",
    )
    path = tmp_path / "Dictionary.yaml"
    save_models_index(path, index)
    assert load_models_index(path) == index


def test_documents_index_roundtrip(tmp_path):
    index = DocumentsIndex(documents=[
        DocumentEntry(name="en", path="content/en.md", hash_c="aaa", hash_d="bbb"),
    ])
    path = tmp_path / "docs.yaml"
    save_documents_index(path, index)
    assert load_documents_index(path) == index


def test_load_store_index_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_store_index(tmp_path / "nonexistent")


def test_save_creates_parent_dirs(tmp_path):
    path = tmp_path / "a" / "b" / "docs.yaml"
    save_documents_index(path, DocumentsIndex())
    assert path.exists()
