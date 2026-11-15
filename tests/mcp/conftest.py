"""Fixtures of the MCP tests: an isolated copy of a real store, and the real server over stdio.

The store is built once with the public API (`mcp_world`); each server serves its own copy of it
in the temporary directory (`/dev/shm` when TMPDIR says so)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator

import pytest

pytest.importorskip("mcp", reason="the `mcp` extra is not installed")

from mcp_session import WRITER, McpSession, copy_of, served, tree_digest  # noqa: E402
from mcp_world import MODULE, build  # noqa: E402


@pytest.fixture(scope="session")
def built_world(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    """The project root of the store every copy comes from."""
    root = tmp_path_factory.mktemp("mcp-world") / "world"
    try:
        yield build(root)
    finally:
        sys.path[:] = [p for p in sys.path if p != str(root)]
        sys.modules.pop(MODULE, None)


@pytest.fixture(scope="session")
def store_copy(built_world: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The copy the read tools are served from; nothing writes to it."""
    return copy_of(built_world, tmp_path_factory, "mcp-read")


@pytest.fixture(scope="session")
def write_copy(built_world: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A second copy, the one the write tools write to."""
    return copy_of(built_world, tmp_path_factory, "mcp-write")


@pytest.fixture(scope="session")
def copy_digest_before(store_copy: Path) -> dict[str, str]:
    """The read copy before the server reads it."""
    return tree_digest(store_copy)


@pytest.fixture(scope="session")
def mcp(store_copy: Path, copy_digest_before: dict[str, str]) -> Iterator[McpSession]:
    """The server at level 0 (the default) over the read copy."""
    with served(store_copy) as session:
        yield session


@pytest.fixture(scope="session")
def writer(write_copy: Path) -> Iterator[McpSession]:
    """The server at write level 2 (content and rules as data) over the write copy."""
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        yield session


@pytest.fixture(scope="session")
def content_writer(write_copy: Path) -> Iterator[McpSession]:
    """The server at write level 1 (content only) over the write copy."""
    with served(write_copy, "--level", "1", "--actor", WRITER) as session:
        yield session
