"""`sldb.api.transaction` and `sldb.api.apply_batch`: writes visible at once, undone together.

The fixture store is `tests/api/conftest.py`'s (TicketDoc, one tracked document `login`); the
moves test registers a referencing pair of models so an incoming edge can be followed.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import pytest

import sldb.api as api
from sldb.api.documents import transaction_ops
from sldb.core.exceptions import ConflictError, SLDBStoreError, SLDBValidationError
from sldb.store.io.rollback import RollbackError
from sldb.store.io import rollback
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path

from .conftest import PAYLOAD

REF_MODULE = "sldb_transaction_ref_models"
REF_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Linked(StructuredNLDoc):
    __references__ = ["about"]
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(default="", description="Referenced document export id.")
'''


def _files(root: Path) -> dict[str, str]:
    """sha256 of every file under the project (lock files aside): bytes, entries and shards."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and "locks" not in p.parts}


def _edges(store: Path) -> list:
    return [e.model_dump() for e in api.load_edge_index(store).edges]


def _title(api_store, name: str) -> str:
    return next(d.payload["title"] for d in api.load_runtime_documents(api_store.store, api_store.pythonpath) if d.name == name)


def _entry(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def _failing_create(monkeypatch, at_call: int):
    """`create_document` as the transaction sees it, raising on call number `at_call`."""
    calls, real = {"n": 0}, transaction_ops.create_document

    def injected(*args: Any, **kwargs: Any):
        calls["n"] += 1
        if calls["n"] == at_call:
            raise SLDBValidationError("injected validation failure")
        return real(*args, **kwargs)

    monkeypatch.setattr(transaction_ops, "create_document", injected)


def test_a_batch_whose_third_change_fails_leaves_bytes_entries_and_index_as_before(api_store, monkeypatch):
    before, edges_before = _files(api_store.root), _edges(api_store.store)
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    _failing_create(monkeypatch, 3)
    changes = [{"id": f"t{i}", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": f"T{i}"}} for i in (1, 2, 3)]
    with pytest.raises(SLDBValidationError, match="injected"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before
    assert _edges(api_store.store) == edges_before
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    assert not (api_store.root / "t1.md").exists() and api.doc_status(api_store.store, "t1").exists is False


def test_nested_transactions_the_inner_ending_well_and_the_outer_failing_revert_both(api_store):
    before = _files(api_store.root)
    with pytest.raises(RuntimeError, match="outer"):
        with api.transaction(api_store.store, api_store.pythonpath) as outer:
            outer.update("login", {**PAYLOAD, "title": "Outer"})
            with api.transaction(api_store.store, api_store.pythonpath) as inner:
                inner.create("TicketDoc", "inner", {**PAYLOAD, "title": "Inner"}, "inner.md")
            assert (api_store.root / "inner.md").exists()
            raise RuntimeError("outer failed")
    assert _files(api_store.root) == before
    assert _title(api_store, "login") == "Broken login"


def test_an_update_is_read_with_its_new_value_inside_the_transaction(api_store):
    with api.transaction(api_store.store, api_store.pythonpath) as tx:
        saved = tx.update("login", {**PAYLOAD, "title": "Inside"})
        assert "# Inside" in saved.path.read_text(encoding="utf-8")
        assert _title(api_store, "login") == "Inside"
    assert _title(api_store, "login") == "Inside"


def test_write_file_with_another_sha256_fails_without_writing(api_store):
    notes = api_store.root / "notes.txt"
    notes.write_text("v1", encoding="utf-8")
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("notes.txt", b"v2", expected_sha256="0" * 64)
    assert (info.value.ref, info.value.expected, info.value.actual) == ("notes.txt", "0" * 64, hashlib.sha256(b"v1").hexdigest())
    assert notes.read_text(encoding="utf-8") == "v1"


def test_write_file_and_record_are_restored_by_the_rollback(api_store):
    (api_store.root / "own.txt").write_text("mine", encoding="utf-8")
    with pytest.raises(RuntimeError):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("new.txt", b"new", expected_sha256=None)
            (api_store.root / tx.record("own.txt")).write_text("changed", encoding="utf-8")
            raise RuntimeError("boom")
    assert not (api_store.root / "new.txt").exists()
    assert (api_store.root / "own.txt").read_text(encoding="utf-8") == "mine"


def test_a_stale_expected_source_hash_is_a_conflict_and_writes_nothing(api_store):
    actual = _entry(api_store, "login").source_hash
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Nope"}, expected_source_hash="stale")
    assert (info.value.ref, info.value.expected, info.value.actual) == ("login", "stale", actual)
    assert _title(api_store, "login") == "Broken login"


def test_the_source_hash_guard_is_checked_before_the_payload_guard(api_store):
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected_source_hash": "stale", "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert info.value.expected == "stale"
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert (info.value.expected, info.value.actual) == ({"title": "also stale"}, PAYLOAD)


def test_a_failure_during_the_rollback_is_raised_with_the_unrestored_paths(api_store, monkeypatch):
    real = rollback._restore

    def refusing(path: Path, data: bytes | None) -> None:
        if path.name == "login.md":
            raise OSError("disk says no")
        real(path, data)

    monkeypatch.setattr(rollback, "_restore", refusing)
    with pytest.raises(RollbackError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Half"})
            raise RuntimeError("original failure")
    assert info.value.unrestored == ["login.md"]
    assert isinstance(info.value.__cause__, RuntimeError) and str(info.value.__cause__) == "original failure"


def test_apply_batch_refuses_everything_when_one_change_is_invalid_and_writes_nothing(api_store):
    before = _files(api_store.root)
    changes = [{"id": "fine", "action": "create", "model": "TicketDoc", "payload": PAYLOAD}, {"id": "login", "action": "update", "payload": {"title": 7}, "expected": PAYLOAD}]
    with pytest.raises(SLDBValidationError, match="login"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before


def test_apply_batch_orders_creates_updates_moves_untracks_and_deletes(api_store):
    api_store.write_document("loose", PAYLOAD)
    api.track_document_file(api_store.store, "TicketDoc", "loose.md", pythonpath=api_store.pythonpath)
    report = api.apply_batch(api_store.store, [
        {"id": "loose", "action": "delete", "expected": PAYLOAD},
        {"id": "login", "action": "move", "path": "moved/login.md", "expected_source_hash": _entry(api_store, "login").source_hash},
        {"id": "fresh", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": "Fresh"}},
        {"id": "untracked", "action": "track", "model": "TicketDoc", "path": str(api_store.write_document("untracked", PAYLOAD).relative_to(api_store.root))},
    ], api_store.pythonpath)
    assert report.saved == ["fresh", "untracked", "login", "loose"]
    assert (api_store.root / "TicketDoc" / "fresh.md").exists() is False and (api_store.root / "fresh.md").exists()
    assert _entry(api_store, "login").path == "moved/login.md" and not (api_store.root / "loose.md").exists()


def test_create_and_move_refuse_a_path_outside_the_project_root(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="outside"):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.create("TicketDoc", "escaped", PAYLOAD, tmp_path / "escaped.md")
    with pytest.raises(SLDBStoreError, match="outside"):
        api.move_document(api_store.store, "login", tmp_path / "login.md", api_store.pythonpath)


@pytest.fixture
def linked_store(tmp_path: Path):
    """`n1` (Note) referenced by `l1` (Linked.about = Note:n1)."""
    (tmp_path / f"{REF_MODULE}.py").write_text(REF_MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("Note", "Linked"):
        api.add_model(store, f"{REF_MODULE}:{model}", str(tmp_path))
    api.create_document(store, "Note", "n1.md", {"title": "n1"}, "n1", str(tmp_path))
    api.create_document(store, "Linked", "l1.md", {"title": "l1", "about": "Note:n1"}, "l1", str(tmp_path))
    yield root, store, str(tmp_path)
    sys.modules.pop(REF_MODULE, None)


def test_move_keeps_the_name_and_the_incoming_edges_keep_resolving(linked_store):
    root, store, py = linked_store
    incoming = [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")]
    assert incoming
    with api.transaction(store, py) as tx:
        moved = tx.move("n1", "notes/n1.md")
    assert (moved.model, moved.name, moved.path) == ("Note", "n1", (root / "notes" / "n1.md").resolve())
    assert not (root / "n1.md").exists()
    assert [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")] == incoming
    assert api.check_store(store, root, py)["ok"]


def test_a_failed_move_puts_the_file_and_the_entry_back(linked_store):
    root, store, py = linked_store
    before = _files(root)
    with pytest.raises(RuntimeError):
        with api.transaction(store, py) as tx:
            tx.move("n1", "notes/n1.md")
            raise RuntimeError("after the move")
    assert _files(root) == before
    assert api.check_store(store, root, py)["ok"]
