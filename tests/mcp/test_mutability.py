"""The write level is the server's: a call above it fails before anything is evaluated; the
write tools take typed arguments only; no tool writes a Python module."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mcp_helpers import an_item
from mcp_session import server_env, tree_digest
from test_read_tools import TOOLS

WRITE_TOOLS = {"propose_changes", "apply_changes"}
#: A change on a rule document that names nothing the store has: evaluating it at all would
#: answer "not registered" or "not a document", not the level.
RULE_CHANGES = [
    {"action": "update", "model": "RuleDoc", "name": "no-such-rule", "fields": {"severity": "error"}},
    {"action": "create", "model": "RelationTypeDoc", "name": "no-such-type", "payload": {}},
]


def test_level_0_serves_no_write_tool_and_naming_one_is_a_signal(mcp) -> None:
    assert {t.name for t in mcp.list_tools()} == TOOLS
    answer = mcp.call("propose_changes", changes=RULE_CHANGES[:1])
    assert answer["signal"] == "unknown_tool" and answer["registered_as_signal"] is True
    assert "write level 1" in answer["explanation"] and "level 0" in answer["explanation"]


def test_level_1_refuses_rules_before_evaluating_anything(content_writer, write_copy: Path) -> None:
    assert {t.name for t in content_writer.list_tools()} == TOOLS | WRITE_TOOLS
    before = tree_digest(write_copy)
    for change in RULE_CHANGES:
        error = content_writer.error_of("propose_changes", changes=[change])
        assert "LevelError" in error and "write level 2" in error and "level 1" in error, error
        assert "register" not in error and "not a document" not in error, error
    assert tree_digest(write_copy) == before


def test_level_1_refuses_to_apply_a_rules_proposal(writer, content_writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    rule = {"title": "x", "subject": f"model <= {item['model']}", "condition": "true", "severity": "alert", "moment": "on_write", "message": ""}
    proposal = writer.call("propose_changes", changes=[{"action": "create", "model": "RuleDoc", "name": "rule-level", "payload": rule, "path": "ruledoc/rule-level.md"}])["proposal"]
    assert proposal["level"] == 2
    error = content_writer.error_of("apply_changes", proposal=proposal)
    assert "LevelError" in error and "write level 2" in error, error


def test_level_1_writes_content(content_writer, write_copy: Path) -> None:
    item = an_item(content_writer, write_copy)
    answer = content_writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": item["payload"]["title"]}}])
    assert answer["proposal"]["level"] == 1


def test_models_as_code_are_never_served(write_copy: Path) -> None:
    done = subprocess.run([sys.executable, "-m", "sldb", "mcp", "--store", str(write_copy / ".sldb"), "--level", "3"], capture_output=True, text=True, timeout=120, env=server_env(), cwd=write_copy)
    assert done.returncode == 2 and "--level" in done.stderr, done.stderr


def test_no_tool_writes_a_python_module(writer, write_copy: Path) -> None:
    assert {t.name for t in writer.list_tools()} == TOOLS | WRITE_TOOLS
    item = an_item(writer, write_copy)
    error = writer.error_of("propose_changes", changes=[{"action": "create", "model": item["model"], "name": "item-module", "payload": item["payload"], "path": "src/item_module.py"}])
    assert "not a Markdown document" in error
    assert not (write_copy / "src").exists()


def test_write_tools_take_typed_arguments_only(writer, write_copy: Path) -> None:
    schema = next(t for t in writer.list_tools() if t.name == "propose_changes").input_schema
    variants = schema["$defs"]
    actions = set()
    for name in ("CreateDocument", "UpdateDocument", "DeleteDocument", "AssertEdge", "RetractEdge"):
        assert variants[name]["additionalProperties"] is False, name
        actions.add(variants[name]["properties"]["action"]["const"])
    assert actions == {"create", "update", "delete", "assert_edge", "retract_edge"}
    item = an_item(writer, write_copy)
    for change in (
        {"action": "make the item say something nicer", "model": item["model"], "name": item["name"]},
        {"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "x"}, "instructions": "and fix its status"},
        "update the item's title",
    ):
        assert "validation error" in writer.error_of("propose_changes", changes=[change]).lower(), change
