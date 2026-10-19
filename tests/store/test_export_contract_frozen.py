"""The on-disk and wire format of a store is a frozen sldb contract.

Readers outside sldb open `.sldb/` and semantic exports that were written long ago: they read
the store index, the document entries and the export by key and by contract name. Renaming
any of these breaks every file already written, silently, so these tests pin the
`sldb_kgdb_semantic_export` v1 contract, the `sldb://...` node ids and the `.sldb/` keys.
A format change goes behind a new contract version, never a rename.
"""
from __future__ import annotations

import json
import sys

import pytest
import yaml

from sldb.cli import main as cli_main
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot

from .test_semantic_export import _build_tracked_store


@pytest.fixture(autouse=True)
def _forget_the_tmp_model_package():
    """The shared helper imports `tmpdocs` from each test's tmp dir; drop it so the next
    test (here or in test_semantic_export) resolves its own copy, not a stale path."""
    yield
    for name in [m for m in sys.modules if m == "tmpdocs" or m.startswith("tmpdocs.")]:
        del sys.modules[name]


def _export(store, root, capsys) -> dict:
    assert cli_main(["stores", "semantic-export", "--store", str(store), "--pythonpath", str(root), "--rebuild"]) == 0
    return json.loads(capsys.readouterr().out)


def test_the_store_index_keeps_its_keys(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    other = tmp_path / "other"
    other.mkdir()
    assert cli_main(["stores", "init", "--path", str(other)]) == 0
    assert cli_main(["stores", "add", str(other / ".sldb"), "--name", "other", "--store", str(store)]) == 0
    index = yaml.safe_load((store / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    assert isinstance(index, dict)
    model = next(m for m in index["models"] if m["name"] == "TaskDoc")
    assert {"name", "model_ref", "path"} <= model.keys()
    assert all(isinstance(model[k], str) for k in ("name", "model_ref", "path"))
    assert [link["name"] for link in index["stores"]] == ["other"]
    assert all({"name", "path"} <= link.keys() for link in index["stores"])


def test_a_document_entry_keeps_its_keys(tmp_path, capsys):
    store, _ = _build_tracked_store(tmp_path, capsys)
    entries = sorted((store / "core" / "documents" / "TaskDoc").glob("*.yaml"))
    assert entries
    entry = yaml.safe_load(entries[0].read_text(encoding="utf-8"))
    assert isinstance(entry["name"], str) and isinstance(entry["path"], str)
    assert isinstance(entry["source_hash"], str) and isinstance(entry["content_hash"], str)
    assert isinstance(entry["semantic_tags"], list)


def test_the_export_keeps_its_contract_name_version_and_keys(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    payload = _export(store, root, capsys)
    assert {k: payload["contract"][k] for k in ("name", "version")} == {"name": "sldb_kgdb_semantic_export", "version": 1}
    assert {"root", "store_path", "hash_a"} <= payload["store"].keys()
    assert {"name", "model_ref", "path", "semantics", "hash_b"} <= payload["models"][0].keys()
    assert {"id", "name", "model", "path", "semantic_tags", "hash_c", "hash_d"} <= payload["documents"][0].keys()
    assert {"id", "document_id", "path", "title", "semantic_tags"} <= payload["sections"][0].keys()
    assert {"nodes", "equivalences"} <= payload["semantic_dag"].keys()


def test_snapshot_ids_keep_the_sldb_uri_forms(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    ids = {node.identity.node_id for node in sldb_semantic_export_to_snapshot(_export(store, root, capsys)).nodes}
    for prefix in ("sldb://store", "sldb://model/TaskDoc", "sldb://document/", "sldb://section/", "sldb://semantic_tag/"):
        assert any(i.startswith(prefix) for i in ids), prefix
