"""Reading through the server writes nothing: not the served copy of the store, and not the
tracked documents. The signal log lives in `.sldb_cache`, which is not store state."""

from __future__ import annotations

from pathlib import Path

from mcp_helpers import an_item
from mcp_session import tree_digest
from test_read_tools import TOOLS


def test_every_read_tool_leaves_the_store_untouched(mcp, store_copy: Path, copy_digest_before: dict[str, str]) -> None:
    called = set()
    item = an_item(mcp, store_copy)["export_id"]
    for tool, arguments in [
        ("list_models", {}),
        ("describe_model", {"model": "Item"}),
        ("list_relation_types", {}),
        ("describe_relation_type", {"name": "moves_to"}),
        ("read_document", {"ref": item}),
        ("read_document", {"ref": item, "field": "status"}),
        ("select_documents", {"model": "Stage", "include_linked": True}),
        ("neighbors", {"node": item, "direction": "outgoing"}),
        ("neighbors", {"node": item, "direction": "incoming"}),
        ("neighborhood", {"node": item, "direction": "both", "depth": 2}),
        ("list_views", {}),
        ("resolve_view", {"view": "board"}),
        ("anchors_resolve", {"target": str(next(store_copy.rglob("*.md")).relative_to(store_copy))}),
        ("check_integrity", {}),
        ("list_signals", {}),
    ]:
        mcp.call(tool, **arguments)
        called.add(tool)
    assert called == {tool.name for tool in mcp.list_tools()} == TOOLS
    changed = sorted(path for path in set(copy_digest_before) | set(tree_digest(store_copy)) if copy_digest_before.get(path) != tree_digest(store_copy).get(path))
    assert not changed, f"reading wrote to: {changed}"


def test_logging_a_signal_is_not_a_write_to_the_store(mcp, store_copy: Path, copy_digest_before: dict[str, str]) -> None:
    before = mcp.call("list_signals")["total"]
    assert mcp.call("describe_model", model="NoSuchModelDoc")["registered_as_signal"] is True
    assert mcp.call("list_signals")["total"] == before + 1
    assert (store_copy / ".sldb_cache" / "signals.jsonl").is_file()
    assert tree_digest(store_copy) == copy_digest_before
