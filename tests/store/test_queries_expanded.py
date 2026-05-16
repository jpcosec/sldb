import pytest
from sldb.store.query import (
    list_structural,
    get_structural,
    glob_structural,
    find_structural,
    list_semantic,
    glob_semantic,
    get_global_semantic,
)
from sldb.models.structured_doc import StructuredNLDoc
from pydantic import Field


class MockModel(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•content⸥"
    title: str = Field(description="Title")
    content: str = Field(description="Content")


def mock_resolve_model_ref(model_ref, pythonpath=None):
    return MockModel


@pytest.fixture
def populated_store(tmp_path):
    store_path = tmp_path / ".sldb"
    store_path.mkdir()

    # Create a minimal store structure
    (store_path / "store_index.yaml").write_text("models: []\nstores: []\n")
    (store_path / "semantic_index.yaml").write_text("tags: {}\ndocuments: {}\n")
    (store_path / "semantic_dag.yaml").write_text("equivalences: {}\n")

    return store_path


def test_structural_list_root(populated_store):
    res = list_structural(populated_store, "st", mock_resolve_model_ref)
    assert isinstance(res, list)


def test_structural_list_invalid_address(populated_store):
    res = list_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res == []


def test_get_structural_invalid_address(populated_store):
    res = get_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res is None


def test_glob_structural_invalid_pattern(populated_store):
    res = glob_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res == []


def test_find_structural_invalid_address(populated_store):
    res = find_structural(
        populated_store, "invalid", "title='x'", mock_resolve_model_ref
    )
    assert res == []


def test_semantic_list_root(populated_store):
    # This will trigger rebuild_semantic_indexes because semantic_index is empty
    res = list_semantic(populated_store, "se", mock_resolve_model_ref)
    assert res == []


def test_glob_semantic_empty(populated_store):
    res = glob_semantic(populated_store, "se.*", mock_resolve_model_ref)
    assert res == []


def test_get_global_semantic_empty(populated_store):
    res = get_global_semantic(populated_store, "gse.type", mock_resolve_model_ref)
    assert res == []


class BaseDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title")


class ChildDoc(BaseDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•child_field⸥"
    child_field: str = Field(description="Child field")


def test_model_inheritance_query(tmp_path):
    # Setup a store with a base and child model
    project_root = tmp_path
    store_path = project_root / ".sldb"
    store_path.mkdir()

    # Mocking necessary files for store to function
    (store_path / "store_index.yaml").write_text("models: []\nstores: []\n")
    (store_path / "semantic_index.yaml").write_text("tags: {}\ndocuments: {}\n")
    (store_path / "semantic_dag.yaml").write_text("equivalences: {}\n")

    # In a real scenario we'd use CLI to add these, but we can simulate the runtime list
    from sldb.store.query import RuntimeDocument

    doc1 = RuntimeDocument(
        store_name="local",
        store_path=store_path,
        model_name="BaseDoc",
        model_type=BaseDoc,
        name="doc1",
        path="doc1.md",
        payload={"title": "Base"},
        semantic_tags=["type.base"],
    )
    doc2 = RuntimeDocument(
        store_name="local",
        store_path=store_path,
        model_name="ChildDoc",
        model_type=ChildDoc,
        name="doc2",
        path="doc2.md",
        payload={"title": "Child", "child_field": "x"},
        semantic_tags=["type.child"],
    )

    # We need to monkeypatch load_runtime_documents or just test functions that take docs if they existed
    # Since we can't easily monkeypatch in this tool, let's focus on unit testing where we can.

    import sldb.store.query

    # Manual injection for testing internal logic
    sldb.store.query.load_runtime_documents = lambda *args, **kwargs: [doc1, doc2]

    # Test recursive listing (st.{BaseDoc+})
    res = list_structural(store_path, "st.{BaseDoc+}", lambda *a: BaseDoc)
    assert "doc1" in res
    assert "doc2" in res

    # Test non-recursive listing (st.{BaseDoc})
    res = list_structural(store_path, "st.{BaseDoc}", lambda *a: BaseDoc)
    assert "doc1" in res
    assert "doc2" not in res
