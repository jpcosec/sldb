import pytest
from sldb.store.models import (
    DocSections,
    DocumentEntry,
    DocumentsIndex,
    ModelEntry,
    ModelsIndex,
    SectionContextRecord,
    SectionsIndex,
    StoreEntry,
    StoreIndex,
)
from sldb.store.io import (
    load_sections_index,
    load_store_index,
    save_models_index,
    save_sections_index,
    save_store_index,
    load_documents_index,
    load_models_index,
    save_documents_index,
)


def test_store_index_roundtrip(tmp_path):
    index = StoreIndex(
        stores=[StoreEntry(name="shared", path="~/.sldb")],
        models=[
            ModelEntry(
                name="Book",
                model_ref="myapp.models:Book",
                path="src/models/book.py",
                models_index=".sldb/models/Book.yaml",
            )
        ],
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
        name="Dictionary",
        model_ref="myapp.models:Dictionary",
        path="src/models/dictionary.py",
        documents_index=".sldb/documents/Dictionary.yaml",
        hash_b="def456",
    )
    path = tmp_path / "Dictionary.yaml"
    save_models_index(path, index)
    assert load_models_index(path) == index


def test_documents_index_roundtrip(tmp_path):
    index = DocumentsIndex(
        documents=[
            DocumentEntry(name="en", path="content/en.md", hash_c="aaa", hash_d="bbb"),
        ]
    )
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


def test_sections_index_roundtrip(tmp_path):
    index = SectionsIndex(
        documents=[
            DocSections(
                doc_name="roadmap",
                sections=[
                    SectionContextRecord(
                        path="roadmap",
                        title="Roadmap",
                        breadcrumbs=["Roadmap"],
                        about=["Roadmap", "roadmap"],
                        semantic_tags=["doc"],
                    ),
                ],
            ),
        ]
    )
    path = tmp_path / "sections_index.yaml"
    save_sections_index(path, index)
    loaded = load_sections_index(path)
    assert loaded == index
    assert loaded.documents[0].sections[0].title == "Roadmap"


def test_sections_index_empty_defaults(tmp_path):
    loaded = load_sections_index(tmp_path / "nonexistent.yaml")
    assert loaded.documents == []
