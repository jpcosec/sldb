"""Asking for what does not exist is a signal: logged, answered with near names, listed by
`list_signals`, and never an error. The log lives in the store's cache."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from mcp_helpers import an_item, page_items
from mcp_session import WRITER, tree_digest
from sldb.mcp.signals import CLASSES, PENDING_TOOLS

CLOSED_CATALOG = {"unknown_tool", "unknown_model", "unknown_document", "unknown_field", "unknown_relation", "unknown_view", "unknown_argument", "not_implemented"}


def raw_call(session, tool: str, **arguments: Any) -> Any:
    """The result of a call as the client receives it, without turning an error into a failure."""
    return session.portal.call(lambda: session.client.call_tool(tool, arguments))


def logged(store: Path) -> list[dict[str, Any]]:
    """The log file of the store, line by line."""
    return [json.loads(line) for line in (store / ".sldb_cache" / "signals.jsonl").read_text(encoding="utf-8").splitlines()]


def newest(session, count: int = 1) -> list[dict[str, Any]]:
    """The last `count` signals `list_signals` reports."""
    return page_items(session, "list_signals")[-count:]


def test_the_catalog_is_closed() -> None:
    assert set(CLASSES) == CLOSED_CATALOG
    assert "undo_changes" in PENDING_TOOLS


def test_unknown_names_are_signals_and_not_errors(mcp, store_copy: Path) -> None:
    item = an_item(mcp, store_copy)
    cases = [
        ("unknown_model", "describe_model", {"model": "Itm"}, "Item"),
        ("unknown_model", "select_documents", {"model": "Stag"}, "Stage"),
        ("unknown_document", "read_document", {"ref": "Item:i01"}, "Item:i1"),
        ("unknown_field", "read_document", {"ref": item["export_id"], "field": "statu"}, "status"),
        ("unknown_relation", "describe_relation_type", {"name": "move_to"}, "moves_to"),
        ("unknown_relation", "neighbors", {"node": item["export_id"], "relation": "reference"}, "references"),
        ("unknown_document", "neighbors", {"node": "Item:i01"}, "Item:i1"),
        ("unknown_view", "resolve_view", {"view": "bord"}, "board"),
    ]
    for signal_class, tool, arguments, near in cases:
        answer = mcp.call(tool, **arguments)
        assert answer["signal"] == signal_class and answer["registered_as_signal"] is True, (tool, arguments, answer)
        assert near in answer["suggestions"] and len(answer["suggestions"]) <= 5, (tool, answer["suggestions"])
        assert "registered as a signal" in answer["explanation"], answer


def test_every_signal_reaches_the_log_with_its_entry(mcp, store_copy: Path) -> None:
    before = len(logged(store_copy)) if (store_copy / ".sldb_cache" / "signals.jsonl").exists() else 0
    answer = mcp.call("describe_model", model="Itm")
    [entry] = logged(store_copy)[before:]
    assert set(entry) == {"at", "tool", "arguments", "signal_class", "suggestions", "actor"}
    assert entry["tool"] == "describe_model" and entry["arguments"]["model"] == "Itm"
    assert entry["signal_class"] == "unknown_model" and entry["suggestions"] == answer["suggestions"]
    assert entry["actor"] is None
    assert datetime.fromisoformat(entry["at"].replace("Z", "+00:00")).utcoffset().total_seconds() == 0 and entry["at"].endswith("Z")
    assert newest(mcp)[0] == entry


def test_list_signals_is_paged_and_filtered(mcp) -> None:
    for name in ("Itm", "Stge", "Rule"):
        mcp.call("describe_model", model=name)
    mcp.call("describe_relation_type", name="move_to")
    everything = page_items(mcp, "list_signals", limit=2)
    assert everything == page_items(mcp, "list_signals", limit=500) and len(everything) > 2
    first = mcp.call("list_signals", limit=2)
    assert first["truncated"] and first["next_offset"] == 2 and first["total"] == len(everything)
    models = page_items(mcp, "list_signals", signal_class="unknown_model")
    assert models and {e["signal_class"] for e in models} == {"unknown_model"}
    assert models == [e for e in everything if e["signal_class"] == "unknown_model"]
    assert "signal_class" in mcp.error_of("list_signals", signal_class="no_such_class")


def test_an_unknown_tool_is_a_signal_with_near_tool_names(mcp) -> None:
    result = raw_call(mcp, "select_document", model="Item")
    assert result.is_error is False
    answer = result.structured_content
    assert answer["signal"] == "unknown_tool" and "select_documents" in answer["suggestions"]
    assert newest(mcp)[0]["tool"] == "select_document" and newest(mcp)[0]["signal_class"] == "unknown_tool"


def test_an_unknown_argument_is_a_signal_and_nothing_runs(mcp, store_copy: Path) -> None:
    result = raw_call(mcp, "select_documents", modle="Item")
    assert result.is_error is False
    answer = result.structured_content
    assert answer["signal"] == "unknown_argument" and answer["unknown_arguments"] == ["modle"] and "model" in answer["suggestions"]
    entry = newest(mcp)[0]
    assert entry["tool"] == "select_documents" and entry["arguments"] == {"modle": "Item"} and entry["signal_class"] == "unknown_argument"


def test_undo_changes_is_a_not_implemented_signal(mcp) -> None:
    assert "undo_changes" not in {t.name for t in mcp.list_tools()}
    result = raw_call(mcp, "undo_changes", proposal={})
    assert result.is_error is False
    answer = result.structured_content
    assert answer["signal"] == "not_implemented" and "20261115-123855" in answer["explanation"]
    entry = newest(mcp)[0]
    assert (entry["tool"], entry["signal_class"]) == ("undo_changes", "not_implemented")


def test_a_found_answer_logs_nothing(mcp, store_copy: Path) -> None:
    before = mcp.call("list_signals")["total"]
    mcp.call("describe_model", model="Item")
    mcp.call("read_document", ref=an_item(mcp, store_copy)["export_id"])
    assert mcp.call("list_signals")["total"] == before


def test_the_log_is_not_the_stores_state(mcp, store_copy: Path, copy_digest_before: dict[str, str]) -> None:
    mcp.call("describe_model", model="Itm")
    assert tree_digest(store_copy) == copy_digest_before
    assert (store_copy / ".sldb_cache" / "signals.jsonl").is_file()
    assert not list((store_copy / ".sldb").rglob("signals*"))


def test_the_writer_signs_its_signals_and_a_missing_level_is_explained(writer, write_copy: Path) -> None:
    answer = writer.call("read_document", ref="Item:no-such-item")
    assert answer["signal"] == "unknown_document"
    [entry] = [e for e in logged(write_copy) if e["arguments"].get("ref") == "Item:no-such-item"]
    assert entry["actor"] == WRITER
