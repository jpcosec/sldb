"""The real MCP client, connected over stdio to the real `sldb mcp` server, driven from sync tests."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import pytest

import sldb

SRC = Path(sldb.__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CACHE = ".sldb_cache"
TOOL_TIMEOUT = 300
#: Who the write tests' server says it is; every document it writes must carry it.
WRITER = "agent:sldb-mcp-tests"


def tree_digest(root: Path) -> dict[str, str]:
    """sha256 of every file under `root`; caches are left out: they are regenerable and not the store's state."""
    skipped = {CACHE, "__pycache__"}
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and not skipped & set(p.relative_to(root).parts)}


class McpSession:
    """A client session; tools are called by name with keyword arguments."""

    def __init__(self, portal: Any, client: Any) -> None:
        self.portal = portal
        self.client = client

    def list_tools(self) -> list[Any]:
        return self.portal.call(self.client.list_tools).tools

    def call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        """The tool's structured JSON answer; a tool error fails the test with its message."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        if result.is_error:
            pytest.fail(f"{tool}({arguments}) failed: {result.content}")
        return result.structured_content

    def error_of(self, tool: str, **arguments: Any) -> str:
        """The error text of a call that must fail."""
        result = self.portal.call(lambda: self.client.call_tool(tool, arguments))
        assert result.is_error, f"{tool}({arguments}) did not fail: {result.structured_content}"
        return " ".join(getattr(c, "text", "") for c in result.content)


def server_env(extra_path: tuple[Path, ...] = ()) -> dict[str, str]:
    """The environment of the server process: `sldb` importable from this checkout, by absolute path."""
    paths = [str(SRC), *map(str, extra_path), *filter(None, os.environ.get("PYTHONPATH", "").split(os.pathsep))]
    return {**os.environ, "PYTHONPATH": os.pathsep.join(str(Path(p).resolve()) for p in paths)}


@contextmanager
def served(root: Path, *options: str, extra_path: tuple[Path, ...] = ()) -> Iterator[McpSession]:
    """A session with `python -m sldb mcp --store <root>/.sldb <options>`, launched by stdio."""
    from anyio.from_thread import start_blocking_portal
    from mcp import Client, StdioServerParameters

    params = StdioServerParameters(command=sys.executable, args=["-m", "sldb", "mcp", "--store", str(root / ".sldb"), *options], cwd=str(root), env=server_env(extra_path))
    with start_blocking_portal() as portal:
        with portal.wrap_async_context_manager(Client(params, read_timeout_seconds=TOOL_TIMEOUT)) as client:
            yield McpSession(portal, client)


def copy_of(source: Path, tmp_path_factory: pytest.TempPathFactory, name: str) -> Path:
    """An isolated copy of the world: its caches are not copied (the edge index is rebuilt by the public CLI)."""
    root = tmp_path_factory.mktemp(name) / "world"
    shutil.copytree(source, root, ignore=shutil.ignore_patterns(CACHE, "__pycache__"), symlinks=True)
    done = subprocess.run([sys.executable, "-m", "sldb", "edges", "rebuild", "--store", ".sldb"], cwd=root, env=server_env(), capture_output=True, text=True)
    assert done.returncode == 0, f"edges rebuild failed:\n{done.stdout}\n{done.stderr}"
    return root
