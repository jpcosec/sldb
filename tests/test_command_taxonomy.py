"""docs/architecture/command-taxonomy.md names every operation of every face exactly once.

The four faces are read from the code: `sldb.api.__all__`, the leaf commands of the CLI parser,
the route literals of `sldb serve` and the tools `sldb mcp` registers. A name added to a face
without a row, or a row naming something a face no longer has, fails here.
"""

from __future__ import annotations

import argparse
import ast
import re
from collections import Counter
from pathlib import Path

import sldb.api
from sldb.cli.parser import build_parser

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "architecture" / "command-taxonomy.md"
SERVE = ROOT / "src" / "sldb" / "cli" / "serve"
MCP_REGISTRY = ROOT / "src" / "sldb" / "mcp" / "registry.py"

FACES = ("sldb.api", "CLI", "serve", "mcp")
NO_OPERATION_FACE = {"api": "sldb.api", "cli": "CLI", "serve": "serve", "mcp": "mcp"}
ROUTE = re.compile(r"^(GET|POST) (/\S*)$")


def _ticks(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


def _rows(text: str) -> list[list[str]]:
    return [[c.strip() for c in line.strip().strip("|").split("|")]
            for line in text.splitlines() if line.startswith("|") and not line.startswith("|---")]


def documented() -> dict[str, list[str]]:
    """Every name per face, as often as the document writes it."""
    text = DOC.read_text(encoding="utf-8")
    operations, _, rest = text.partition("## Sin operación")
    names: dict[str, list[str]] = {face: [] for face in FACES}
    header: list[str] = []
    for row in _rows(operations):
        if row[0] == "Operación":
            header = row
            continue
        for face in FACES:
            cell = row[header.index(face)]
            names[face] += _ticks(cell)
    for row in _rows(rest.split("\n## ", 1)[0]):
        if row[0] == "Nombres":
            continue
        names[NO_OPERATION_FACE[row[1]]] += _ticks(row[0])
    return names


def cli_leaves() -> set[str]:
    leaves: set[str] = set()

    def walk(parser: argparse.ArgumentParser, path: list[str]) -> None:
        subs = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
        if not subs:
            leaves.add(" ".join(path))
        for action in subs:
            for name, sub in action.choices.items():
                walk(sub, path + [name])

    walk(build_parser(), [])
    return leaves


def serve_paths() -> set[str]:
    """Route literals of `sldb serve`; a literal ending in `/` is a prefix, not a route."""
    paths: set[str] = set()
    for source in SERVE.glob("*.py"):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                    and re.fullmatch(r"/[a-z][a-z0-9/_-]*", node.value) and not node.value.endswith("/"):
                paths.add(node.value)
    return paths | {"/views/{name}"}


def mcp_tools() -> set[str]:
    tree = ast.parse(MCP_REGISTRY.read_text(encoding="utf-8"))
    tools: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "READ_TOOLS" for t in node.targets):
            tools |= {e.value for e in node.value.elts}
        if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "add_tool" \
                and isinstance(node.args[0], ast.Attribute):
            tools.add(node.args[0].attr)
    return tools


def _once(names: list[str]) -> list[str]:
    return sorted(name for name, n in Counter(names).items() if n > 1)


def test_every_name_appears_exactly_once():
    names = documented()
    assert {face: _once(names[face]) for face in FACES} == {face: [] for face in FACES}


def test_api_matches_the_document():
    assert sorted(set(documented()["sldb.api"]) ^ set(sldb.api.__all__)) == []


def test_cli_matches_the_document():
    assert sorted(set(documented()["CLI"]) ^ cli_leaves()) == []


def test_serve_matches_the_document():
    routes = documented()["serve"]
    malformed = [r for r in routes if not ROUTE.match(r)]
    assert malformed == []
    assert sorted({ROUTE.match(r).group(2) for r in routes} ^ serve_paths()) == []


def test_mcp_matches_the_document():
    assert sorted(set(documented()["mcp"]) ^ mcp_tools()) == []


def test_each_row_is_one_operation_with_a_ring_and_an_effect():
    operations = DOC.read_text(encoding="utf-8").partition("## Sin operación")[0]
    rows = [r for r in _rows(operations) if r[0] != "Operación"]
    assert _once([r[0] for r in rows]) == []
    assert [r[0] for r in rows if not re.fullmatch(r"[a-z]+(_[a-z]+)+|search", r[0])] == []
    assert [r[0] for r in rows if r[1] not in {"0a", "0b", "1", "2", "3", "caras"}] == []
    assert [r[0] for r in rows if r[2] not in {"lee", "escribe", "externo"}] == []
