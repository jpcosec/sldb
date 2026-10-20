"""Provenance in the index (docs/architecture/provenance.md, stage 2): each document entry
records its `sldb` block, the export and `find` expose it, and `--where` reads it as `sldb.<key>`."""
from __future__ import annotations

import json

import yaml

import sldb.api as api
from sldb.cli import main as cli_main
from sldb.models.provenance_block import attach_block
from sldb.store.io import invalidate_index_cache

from .conftest import PAYLOAD


def _entry(api_store, name: str) -> dict:
    return yaml.safe_load((api_store.store / "core" / "documents" / "TicketDoc" / f"{name}.yaml").read_text(encoding="utf-8"))


def test_the_entry_records_the_block_and_none_when_the_document_has_none(api_store):
    api.create_document(api_store.store, "TicketDoc", api_store.root / "new.md", PAYLOAD, "new", api_store.pythonpath, actor="human:jp")
    recorded = _entry(api_store, "new")["provenance"]
    assert recorded["by"] == "human:jp" and recorded["authority"] == "generated" and recorded["via"] == "create_document"
    assert _entry(api_store, "login")["provenance"] is None, "tracked by hand, no block: nothing is invented"


def test_stores_update_reads_a_block_added_by_hand(api_store):
    path = api_store.root / "login.md"
    path.write_text(attach_block(path.read_text(encoding="utf-8"), {"by": "human:jp", "at": "2026-10-20T10:00:00Z", "authority": "source_raw"}), encoding="utf-8")
    api.update_store_indexes(api_store.store, api_store.pythonpath)
    invalidate_index_cache()
    assert _entry(api_store, "login")["provenance"] == {"by": "human:jp", "at": "2026-10-20T10:00:00Z", "authority": "source_raw"}


def test_the_export_and_find_carry_it_and_where_reads_it_by_dotted_path(api_store, capsys):
    api.create_document(api_store.store, "TicketDoc", api_store.root / "raw.md", {**PAYLOAD, "title": "Raw"}, "raw", api_store.pythonpath, actor="human:jp")
    path = api_store.root / "raw.md"
    path.write_text(attach_block(path.read_text(encoding="utf-8"), {"by": "human:jp", "at": 0, "authority": "source_raw"}), encoding="utf-8")
    api.update_store_indexes(api_store.store, api_store.pythonpath)
    invalidate_index_cache()
    args = ["--store", str(api_store.store), "--pythonpath", api_store.pythonpath]
    assert cli_main(["stores", "semantic-export", *args, "--rebuild"]) == 0
    docs = {d["name"]: d for d in json.loads(capsys.readouterr().out)["documents"]}
    assert docs["raw"]["provenance"]["authority"] == "source_raw" and docs["login"]["provenance"] is None
    assert cli_main(["find", "TicketDoc", "--type", "doc", "--where", 'sldb.authority = "source_raw"', *args, "--format", "json"]) == 0
    results = json.loads(capsys.readouterr().out)["results"]
    assert [r["name"] for r in results] == ["raw"] and results[0]["provenance"]["by"] == "human:jp"
    assert cli_main(["find", "TicketDoc", "--type", "doc", "--where", 'sldb.by = "nobody"', *args, "--format", "json"]) == 1
