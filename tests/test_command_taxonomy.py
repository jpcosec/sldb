"""docs/architecture/command-taxonomy.md lists every operation of sldb once.

The names of the four faces are read from the code, not from the document: `sldb.api.__all__`,
the argparse tree behind `sldb`, the route literals of `src/sldb/cli/serve/` and the tools
`sldb.mcp.registry` registers. Each must sit in exactly one row of the document or in its
"Sin operación" list; the marks of a row (duplicado, renombre, hueco) must agree with its cells.
"""

from __future__ import annotations

import argparse
import ast
import re
from collections import Counter
from pathlib import Path

import pytest

import sldb.api
from sldb.cli.parser import build_parser

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "architecture" / "command-taxonomy.md"
FACES = ("api", "cli", "serve", "mcp")
PERMISSIONS = ("lee", "escribe-store", "efecto-externo")
ROUTE = re.compile(r"^/[a-z][a-z0-9_-]*(/[a-z0-9_<>.-]+)*$")
VIEW_BY_NAME = "/views/<name>"  # `views_routes.dispatch_views` strips the prefix; no literal carries it


def api_names() -> set[str]:
    return set(sldb.api.__all__)


def cli_leaves() -> tuple[set[str], set[str]]:
    """(visible leaves, hidden leaves): a leaf is a subcommand with no subcommands of its own."""
    visible: set[str] = set()
    hidden: set[str] = set()

    def walk(parser: argparse.ArgumentParser, path: list[str], is_hidden: bool) -> None:
        actions = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
        if not actions:
            (hidden if is_hidden else visible).add(" ".join(path))
            return
        for action in actions:
            helps = {c.dest: c.help for c in action._choices_actions}
            seen: set[int] = set()
            for name, sub in action.choices.items():
                if id(sub) in seen:
                    continue  # an alias of a parser already walked
                seen.add(id(sub))
                walk(sub, [*path, name], is_hidden or helps.get(name, argparse.SUPPRESS) is argparse.SUPPRESS)

    walk(build_parser(), [], False)
    return visible, hidden


def serve_routes() -> set[str]:
    """Every route path literal in `sldb.cli.serve`, plus the `/views/<name>` family."""
    paths = {VIEW_BY_NAME}
    for source in sorted((ROOT / "src" / "sldb" / "cli" / "serve").glob("*.py")):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and ROUTE.match(node.value):
                paths.add(node.value)
    return paths


def mcp_tools() -> set[str]:
    """The tools `sldb.mcp.registry` registers, read from its source (the `mcp` extra is optional)."""
    tree = ast.parse((ROOT / "src" / "sldb" / "mcp" / "registry.py").read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "READ_TOOLS" for t in node.targets):
            names.update(ast.literal_eval(node.value))
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "add_tool" and node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Attribute):
                names.add(arg.attr)
    return names


def code_names() -> dict[str, set[str]]:
    return {"api": api_names(), "cli": cli_leaves()[0] | cli_leaves()[1], "serve": serve_routes(), "mcp": mcp_tools()}


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _tokens(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


def _route_path(token: str) -> str:
    method, _, path = token.partition(" ")
    assert set(method.split(",")) <= {"GET", "POST"}, f"route without method: {token!r}"
    return path


def parse_doc() -> tuple[list[dict], list[tuple[str, str, str]]]:
    """(operation rows, sin-operación rows) of the document."""
    rows: list[dict] = []
    nothing: list[tuple[str, str, str]] = []
    section = ""
    for line in DOC.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if not line.startswith("|") or set(line) <= set("|- :"):
            continue
        cells = _cells(line)
        if section == "Operaciones" and cells[0] != "Operación":
            op, noun, verb, access, perm, api, cli, serve, mcp, marks = cells[:10]
            rows.append({"op": op.strip("`"), "noun": noun, "verb": verb, "access": access, "perm": perm,
                         "faces": {"api": _tokens(api), "cli": _tokens(cli), "serve": _tokens(serve), "mcp": _tokens(mcp)},
                         "marks": marks})
        elif section == "Sin operación" and cells[0] != "Cara":
            nothing.append((cells[0], *(_tokens(cells[1]) or [""]), cells[2]))
    return rows, nothing[:]


def _documented() -> dict[str, list[str]]:
    rows, nothing = parse_doc()
    found: dict[str, list[str]] = {face: [] for face in FACES}
    for row in rows:
        for face in FACES:
            found[face] += [_route_path(t) if face == "serve" else t for t in row["faces"][face]]
    for face, name, _reason in nothing:
        found[face].append(_route_path(name) if face == "serve" else name)
    return found


@pytest.mark.parametrize("face", FACES)
def test_every_name_of_the_code_is_in_exactly_one_place(face: str) -> None:
    documented = Counter(_documented()[face])
    code = code_names()[face]
    assert code - set(documented) == set(), f"{face}: in the code, missing from {DOC.name}: {sorted(code - set(documented))}"
    assert set(documented) - code == set(), f"{face}: in {DOC.name}, not in the code: {sorted(set(documented) - code)}"
    assert [n for n, k in documented.items() if k > 1] == [], f"{face}: listed more than once"


def test_hidden_cli_leaves_are_listed_as_without_operation() -> None:
    _rows, nothing = parse_doc()
    listed = {name for face, name, _ in nothing if face == "cli"}
    assert cli_leaves()[1] <= listed


def test_every_row_has_noun_verb_access_permission_and_reason_for_exclusions() -> None:
    rows, nothing = parse_doc()
    assert rows
    for row in rows:
        assert row["op"] == f"{row['noun']}_{row['verb']}", row["op"]
        assert re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)+", row["op"]), row["op"]
        assert row["perm"] in PERMISSIONS, row
        assert row["access"] == ("lee" if row["perm"] == "lee" else "escribe"), row
    assert len({r["op"] for r in rows}) == len(rows), "canonical names repeat"
    assert all(reason.strip() for _f, _n, reason in nothing)


def test_marks_agree_with_the_cells() -> None:
    for row in parse_doc()[0]:
        faces = row["faces"]
        marks = row["marks"]
        assert ("duplicado" in marks) == any(len(faces[f]) > 1 for f in FACES), row["op"]
        assert ("renombre" in marks) == any(t != row["op"] for f in ("api", "mcp") for t in faces[f]), row["op"]
        missing = [f for f in FACES if not faces[f]]
        match = re.search(r"hueco: ([a-z, ]+)", marks)
        assert (match.group(1).split(", ") if match else []) == missing, row["op"]


def test_the_document_says_what_it_reuses() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "SurfaceDoc" in text and "selfdoc" in text
