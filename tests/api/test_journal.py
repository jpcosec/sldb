"""The write journal was retired on 2026-11-04: no write produces one, and `sldb journal` says
where the store's past is read now (`sldb docs history <doc>`; `.sldb/` is versioned whole)."""

from __future__ import annotations

import sldb.api as api
from sldb.api.journal import RETIRED_NOTICE
from sldb.cli import main
from sldb.store.layout import cache_dir

from .conftest import PAYLOAD

NOTICE = "El journal fue retirado el 2026-11-04; el pasado del store se consulta con sldb docs history <doc>."


def _journal_dirs(store) -> list:
    return [p for p in (cache_dir(store) / "journal", store / "runtime") if p.exists()]


def test_no_write_leaves_a_journal(api_store):
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "A"}, api_store.pythonpath, actor="pron-turn-1")
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    api.create_document(api_store.store, "TicketDoc", "created.md", PAYLOAD, pythonpath=api_store.pythonpath)
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath, backfill=True)
    api.reindex_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert _journal_dirs(api_store.store) == []
    assert not (cache_dir(api_store.store) / "locks" / "journal.lock").exists()


def test_the_readers_answer_empty(api_store):
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "A"}, api_store.pythonpath)
    assert api.journal(api_store.store) == []
    report = api.verify_journal(api_store.store)
    assert (report.valid, report.entries, report.store) == (True, 0, str(api_store.store))


def test_journal_show_prints_the_notice_and_exits_0(api_store, capsys):
    assert RETIRED_NOTICE == NOTICE
    assert main(["journal", "show", "--store", str(api_store.store)]) == 0
    assert capsys.readouterr().out.strip() == NOTICE
    assert main(["journal", "show", "--store", str(api_store.store), "--limit", "3", "--format", "json"]) == 0
    assert capsys.readouterr().out.strip() == NOTICE


def test_journal_verify_prints_the_same_notice(api_store, capsys):
    assert main(["journal", "verify", "--store", str(api_store.store)]) == 0
    assert capsys.readouterr().out.strip() == NOTICE
