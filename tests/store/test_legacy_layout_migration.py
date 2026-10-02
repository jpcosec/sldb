"""A store from before `.sldb/core` existed keeps every index at the store root.

`open_store` migrates a store it finds (`migrate_store_layout`), but that migration started by
loading `core/store_index.yaml`, so on a root-level store it raised `FileNotFoundError: No
store_index.yaml` before migrating anything and `open_store` crashed. Any command against such
a store was unusable, and the files stayed untouched.

The legacy layout is written into its own directory: hand-editing a store the process already
read would leave every process-wide cache (documents, runtime, io) pointing at a layout that no
longer exists on disk, which is a test artefact and not what a fresh process sees.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_semantic_index,
    load_store_index,
)
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import (
    legacy_semantic_index_path,
    legacy_store_index_path,
    store_index_path,
)
from sldb.store.migration import migrate_store_layout

from tests.store.test_documents_shards import _store


def _legacy_store(tmp_path: Path) -> tuple[Path, Path, dict]:
    """A root-level legacy store built beside the normal one, plus its semantic documents."""
    (tmp_path / "built").mkdir()
    built, built_root = _store(tmp_path / "built", 3)
    before = load_semantic_index(built).documents
    store, root = tmp_path / "legacy" / ".sldb", tmp_path / "legacy"
    (store / "models").mkdir(parents=True)
    (store / "documents").mkdir()
    index = load_store_index(built)
    for model in index.models:
        _write_model_files(store, built_root, model)
        model.models_index = f".sldb/models/{model.name}.yaml"
    (legacy_semantic_index_path(store)).write_text(yaml_dump(load_semantic_index(built).model_dump()), encoding="utf-8")
    (legacy_store_index_path(store)).write_text(yaml_dump(index.model_dump()), encoding="utf-8")
    assert not store_index_path(store).exists()
    return store, root, before


def _write_model_files(store: Path, built_root: Path, model) -> None:
    """One model's legacy index files, pointing at the paths a root-level store would name."""
    model_index = load_models_index(built_root / model.models_index)
    documents = load_documents_index(built_root / model_index.documents_index)
    (store / "documents" / f"{model.name}.yaml").write_text(
        yaml_dump({"documents": [doc.model_dump() for doc in documents.documents]}), encoding="utf-8"
    )
    data = model_index.model_dump()
    data["documents_index"] = f".sldb/documents/{model.name}.yaml"
    data.pop("sections_index", None)
    (store / "models" / f"{model.name}.yaml").write_text(yaml_dump(data), encoding="utf-8")


def test_open_store_migrates_a_root_level_legacy_layout(tmp_path: Path):
    store, root, before = _legacy_store(tmp_path)

    open_store(str(store))

    assert store_index_path(store).exists() and not legacy_store_index_path(store).exists()
    assert not (store / "models").exists() and not (store / "documents").exists()
    assert not legacy_semantic_index_path(store).exists()
    assert load_semantic_index(store).documents == before


def test_migrating_a_root_level_legacy_layout_is_idempotent(tmp_path: Path):
    store, root, _ = _legacy_store(tmp_path)

    assert migrate_store_layout(store, root) is True
    assert migrate_store_layout(store, root) is False


def test_migrated_documents_are_readable_from_the_canonical_index(tmp_path: Path):
    store, root, _ = _legacy_store(tmp_path)
    before = [doc.name for doc in _documents(root, store)]

    open_store(str(store))

    assert sorted(doc.name for doc in _documents(root, store)) == sorted(before)


def _documents(root: Path, store: Path) -> list:
    return [
        doc
        for model in load_store_index(store).models
        for doc in load_documents_index(root / load_models_index(root / model.models_index).documents_index).documents
    ]
