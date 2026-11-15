"""The extension point: a consumer registers tools of its own on the server of sldb and inherits
its level, its actor, its paging and its signal log."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterator

import pytest

from mcp_helpers import files, page_items
from mcp_session import HERE, WRITER, McpSession, copy_of, server_env, served
from mcp_world import ITEM_COUNT
from test_read_tools import TOOLS

EXTENSION_TOOLS = {"count_by_model", "whoami", "find_model"}
SPEC = "example_extension:register"


@pytest.fixture(scope="module")
def extended_copy(built_world: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    return copy_of(built_world, tmp_path_factory, "mcp-extension")


@pytest.fixture(scope="module")
def extended(extended_copy: Path) -> Iterator[McpSession]:
    """The server at level 1 with the example extension, over its own copy."""
    with served(extended_copy, "--level", "1", "--actor", WRITER, "--extension", SPEC, extra_path=(HERE,)) as session:
        yield session


def test_the_extension_tools_join_the_built_in_ones(extended) -> None:
    names = {t.name for t in extended.list_tools()}
    assert names == TOOLS | {"propose_changes", "apply_changes"} | EXTENSION_TOOLS
    described = next(t for t in extended.list_tools() if t.name == "count_by_model")
    assert described.description and described.output_schema is not None


def test_an_extension_tool_pages_like_the_built_in_ones(extended, extended_copy: Path) -> None:
    rows = page_items(extended, "count_by_model", limit=2)
    assert {r["model"]: r["documents"] for r in rows}["Item"] == ITEM_COUNT == len(files(extended_copy, "item"))
    first = extended.call("count_by_model", limit=2)
    assert first["truncated"] and first["next_offset"] == 2 and len(first["items"]) == 2
    assert extended.call("count_by_model", model="Item")["total"] == 1


def test_an_extension_tool_sees_the_level_and_the_actor_of_the_server(extended) -> None:
    assert extended.call("whoami") == {"level": 1, "level_name": "content", "actor": WRITER}


def test_an_extension_tool_inherits_the_signal_log(extended, extended_copy: Path) -> None:
    misspelled = extended.portal.call(lambda: extended.client.call_tool("count_by_model", {"modle": "Item"}))
    assert misspelled.is_error is False and misspelled.structured_content["signal"] == "unknown_argument"
    assert "model" in misspelled.structured_content["suggestions"]
    answer = extended.call("find_model", name="Itm")
    assert answer["signal"] == "unknown_model" and answer["registered_as_signal"] is True and "Item" in answer["suggestions"]
    entries = extended.call("list_signals", limit=500)["items"]
    assert [(e["tool"], e["signal_class"], e["actor"]) for e in entries[-2:]] == [("count_by_model", "unknown_argument", WRITER), ("find_model", "unknown_model", WRITER)]
    assert extended.call("find_model", name="Item")["found"] is True


def test_an_extension_that_does_not_exist_stops_the_server(extended_copy: Path) -> None:
    for spec in ("no_such_module_for_sldb:register", "example_extension:no_such_function", "not-a-spec"):
        done = subprocess.run([sys.executable, "-m", "sldb", "mcp", "--store", str(extended_copy / ".sldb"), "--extension", spec], capture_output=True, text=True, timeout=120, cwd=extended_copy, env=server_env((HERE,)))
        assert done.returncode != 0 and spec.split(":")[0] in done.stderr + done.stdout, (spec, done.stderr)
