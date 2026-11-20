"""`sldb.api` store operations: open, read, link, refresh indexes; and the `sldb.cli` bridges over them."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from sldb.api import extract_payload, link_store, open_store, read_store, store_is_prepared, track_document_file, update_store_indexes
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.runtime.validation import extract_model_data
from sldb.store.io import load_documents_index, load_models_index, load_semantic_index
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import legacy_semantic_index_path, legacy_store_index_path, store_index_path
from sldb.cli import main as cli_main
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index

from tests.api.conftest import MODULE, PAYLOAD
from tests.store.test_documents_shards import _store


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
    assert (linked.name, linked.path) == ("shared", "../other/.sldb")
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


def test_scaffold_store_and_build_store_are_public_and_bridged_by_the_cli(api_store, capsys):
    """GD26: the scaffold of folders and seeds is an `sldb.api` function and a `stores` subcommand."""
    from sldb.api import ScaffoldReport, Seed, StoreDeclaration, build_store, scaffold_store
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import save_declaration

    save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    declaration = StoreDeclaration(folders=["inbox"], seeds=[Seed(path="inbox/.keep", text="")])
    report = scaffold_store(api_store.store, declaration=declaration, apply=True)
    assert isinstance(report, ScaffoldReport) and report.created == ["inbox", "inbox/.keep"]
    assert build_store(api_store.store)["scaffold"] == {"created": [], "rewritten": [], "present": [], "conflicts": []}
    assert cli_main(["stores", "scaffold", "--store", str(api_store.store), "--format", "json"]) == 0
    assert "created" in capsys.readouterr().out


def _snapshot(root: Path) -> set[tuple[str, int, int]]:
    """(path, mtime_ns, size) of every file under `root`."""
    return {(str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in root.rglob("*") if p.is_file()}


def _legacy_store(tmp_path: Path) -> Path:
    """A root-level legacy store, built as `tests/store/test_legacy_layout_migration.py` does."""
    (tmp_path / "built").mkdir()
    built, built_root = _store(tmp_path / "built", 3)
    store = tmp_path / "legacy" / ".sldb"
    (store / "models").mkdir(parents=True)
    (store / "documents").mkdir()
    index = load_store_index(built)
    for model in index.models:
        model_index = load_models_index(built_root / model.models_index)
        documents = load_documents_index(built_root / model_index.documents_index)
        (store / "documents" / f"{model.name}.yaml").write_text(
            yaml_dump({"documents": [doc.model_dump() for doc in documents.documents]}), encoding="utf-8"
        )
        data = model_index.model_dump()
        data["documents_index"] = f".sldb/documents/{model.name}.yaml"
        data.pop("sections_index", None)
        (store / "models" / f"{model.name}.yaml").write_text(yaml_dump(data), encoding="utf-8")
        model.models_index = f".sldb/models/{model.name}.yaml"
    legacy_semantic_index_path(store).write_text(yaml_dump(load_semantic_index(built).model_dump()), encoding="utf-8")
    legacy_store_index_path(store).write_text(yaml_dump(index.model_dump()), encoding="utf-8")
    return store


def test_read_store_writes_nothing_on_a_prepared_store(api_store):
    open_store(api_store.store)
    before = _snapshot(api_store.root)
    assert store_is_prepared(api_store.store)
    location = read_store(api_store.store)
    assert (location.store_path, location.project_root) == (api_store.store.resolve(), api_store.root.resolve())
    assert _snapshot(api_store.root) == before


def test_read_store_refuses_an_unprepared_store_and_leaves_it_unmigrated(tmp_path):
    store = _legacy_store(tmp_path)
    before = _snapshot(store.parent)
    assert not store_is_prepared(store)
    with pytest.raises(SLDBStoreError, match="store not prepared: run `sldb stores update`"):
        read_store(store)
    assert _snapshot(store.parent) == before
    assert legacy_store_index_path(store).exists() and not store_index_path(store).exists()


def test_store_is_prepared_is_false_without_a_store(tmp_path):
    assert not store_is_prepared(tmp_path / ".sldb")


def test_read_store_says_not_found_when_the_store_directory_does_not_exist(tmp_path):
    store = tmp_path / ".sldb"
    with pytest.raises(SLDBStoreError, match=r"^store not found: ") as error:
        read_store(store)
    assert str(store.resolve()) in str(error.value) and "not prepared" not in str(error.value)
    assert not store.exists()


def test_read_store_says_not_prepared_when_the_store_exists_without_its_index(tmp_path):
    store = tmp_path / ".sldb"
    store.mkdir()
    with pytest.raises(SLDBStoreError, match=r"^store not prepared: run `sldb stores update` \("):
        read_store(store)


def test_read_store_sees_a_document_added_by_another_open_store(api_store):
    first = read_store(api_store.store)
    assert [d["name"] for d in indexed_documents(first.store_path)] == ["login"]
    path = api_store.write_document("logout", {**PAYLOAD, "title": "Broken logout"})
    track_document_file(api_store.store, "TicketDoc", path, "logout", api_store.pythonpath)
    second = read_store(api_store.store)
    assert sorted(d["name"] for d in indexed_documents(second.store_path)) == ["login", "logout"]


def test_extract_payload_matches_extract_model_data(api_store):
    from sldb.api import resolve_model_ref

    model_type = resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    markdown = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert extract_payload(model_type, markdown) == extract_model_data(model_type, markdown)
    assert extract_payload(model_type, markdown)["title"] == PAYLOAD["title"]


def _other_store(tmp_path: Path) -> Path:
    other = tmp_path / "other"
    other.mkdir()
    assert cli_main(["stores", "init", "--path", str(other)]) == 0
    return other / ".sldb"


def _add_link(api_store, text: str, *extra: str) -> str:
    assert cli_main(["stores", "add", text, "--name", "other", "--store", str(api_store.store), *extra]) == 0
    return load_store_index(api_store.store).stores[0].path


def _linked(api_store) -> list[Path]:
    from sldb.store.query import _linked_stores

    return [p for p, _ in _linked_stores(api_store.store)]


def test_stores_add_keeps_an_absolute_path_absolute(api_store, tmp_path):
    other = _other_store(tmp_path)
    assert _add_link(api_store, str(other)) == str(other)
    assert _linked(api_store) == [other.resolve()]


def test_stores_add_keeps_a_home_path_as_written_and_reads_it_with_home(api_store, tmp_path, monkeypatch):
    other = _other_store(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert _add_link(api_store, "~/other/.sldb") == "~/other/.sldb"
    assert _linked(api_store) == [other.resolve()]


def test_stores_add_keeps_a_variable_path_as_written_and_reads_it_with_the_variable(api_store, tmp_path, monkeypatch):
    other = _other_store(tmp_path)
    monkeypatch.setenv("SLDB_TEST_ROOT", str(tmp_path))
    assert _add_link(api_store, "$SLDB_TEST_ROOT/other/.sldb") == "$SLDB_TEST_ROOT/other/.sldb"
    assert _linked(api_store) == [other.resolve()]
    assert _add_link(api_store, "${SLDB_TEST_ROOT}/other/.sldb", "--replace") == "${SLDB_TEST_ROOT}/other/.sldb"
    assert cli_main(["stores", "remove", "other", "--store", str(api_store.store)]) == 0
    assert load_store_index(api_store.store).stores == []


def test_stores_add_keeps_a_relative_path_relative_to_the_root(api_store, tmp_path, monkeypatch):
    other = _other_store(tmp_path)
    monkeypatch.chdir(tmp_path)
    rel = _add_link(api_store, "other/.sldb")
    assert rel == os.path.relpath(other, api_store.root)
    assert _linked(api_store) == [other.resolve()]
