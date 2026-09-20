"""The store write journal: one entry per write route, chained and verifiable."""

from __future__ import annotations

import os
import time

import sldb.api as api

from .conftest import MODELS_SOURCE, PAYLOAD

ADD_MODEL_MODULE = "sldb_journal_test_models"


def _ops(store) -> list[str]:
    return [e.operation for e in api.journal(store)]


def _latest(store):
    return api.journal(store, limit=1)[0]


def test_chain_verifies_after_mixed_writes(api_store):
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "A"}, api_store.pythonpath)
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    assert api.verify_journal(api_store.store).valid


def test_each_document_route_leaves_an_entry(api_store):
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "A"}, api_store.pythonpath)
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    api.create_document(api_store.store, "TicketDoc", "created.md", PAYLOAD, pythonpath=api_store.pythonpath)
    assert {"create_document", "save_document_payload", "track_document_file", "untrack_document"} <= set(_ops(api_store.store))


def test_untrack_then_track_repair_leaves_both(api_store):
    api.untrack_document(api_store.store, "login", api_store.pythonpath)
    api.track_document_file(api_store.store, "TicketDoc", api_store.root / "login.md", "login", api_store.pythonpath)
    ops = _ops(api_store.store)
    assert "untrack_document" in ops and "track_document_file" in ops
    assert api.verify_journal(api_store.store).valid


def test_store_without_journal_reads_empty(tmp_path):
    root = tmp_path / "fresh"
    root.mkdir()
    api.init_store(root)
    store = root / ".sldb"
    assert api.journal(store) == []
    assert api.verify_journal(store).valid


def test_add_model_leaves_an_entry(tmp_path):
    (tmp_path / f"{ADD_MODEL_MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    api.init_store(root)
    store = root / ".sldb"
    api.add_model(store, f"{ADD_MODEL_MODULE}:TicketDoc", str(tmp_path))
    assert "add_model" in _ops(store)
    assert api.verify_journal(store).valid


def test_reindex_and_promote_leave_entries(api_store):
    api.reindex_model(api_store.store, "TicketDoc", api_store.pythonpath)
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert {"reindex_model", "promote_model_draft"} <= set(_ops(api_store.store))


def test_save_entry_carries_before_and_after(api_store):
    before = _latest(api_store.store)
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "New"}, api_store.pythonpath, actor="pron-turn-1")
    e = _latest(api_store.store)
    assert (e.operation, e.address, e.actor) == ("save_document_payload", "TicketDoc:login", "pron-turn-1")
    assert e.previous_hash == before.entry_hash
    assert e.previous_value["title"] == "Broken login" and e.new_value["title"] == "New"
    assert e.hash_c_before != e.hash_c_after


def test_write_cost_with_and_without_journal(api_store):
    n = 20
    os.environ["SLDB_JOURNAL_OFF"] = "1"
    try:
        off = _time_writes(api_store, n, "off")
    finally:
        os.environ.pop("SLDB_JOURNAL_OFF", None)
    on = _time_writes(api_store, n, "on")
    assert len(api.journal(api_store.store)) >= n
    print(f"\njournal cost: {n} writes -> off={off:.4f}s on={on:.4f}s overhead={on - off:.4f}s")


def _time_writes(api_store, n: int, label: str) -> float:
    start = time.perf_counter()
    for i in range(n):
        api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": f"{label}-{i}"}, api_store.pythonpath)
    return time.perf_counter() - start
