"""---
id: sldb.selfdoc.cli_tree
kind: core
tags: [system:sldb, workspace:knowledge, topic:selfdoc]

---
Compare the command paths of an argparse tree with the hand-written CLI tree document.

The document keeps one ```text block drawn with ├──, └── and │; each line names
a command, or several joined by `/`, and indentation gives the group it lives in.
This module reads that block and the parser; it never writes either.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

_CONNECTOR = re.compile(r"[├└]── ")
_OPTIONAL = re.compile(r"\s*[\[<].*$")
_HELP = "help"


def parser_paths(parser: argparse.ArgumentParser) -> set[str]:
    """Every group and subcommand path (`stores init`), without aliases, hidden commands or `help`."""
    found: set[str] = set()
    _collect(parser, (), found)
    return found


def _collect(parser, path: tuple[str, ...], found: set[str]) -> None:
    for action in (a for a in parser._actions if isinstance(a, argparse._SubParsersAction)):
        hidden = {i.dest for i in action._choices_actions if i.help == argparse.SUPPRESS}
        seen: set[int] = set()
        for name, child in action.choices.items():
            if id(child) in seen or name in hidden or (name == _HELP and not path):
                continue
            seen.add(id(child))
            found.add(" ".join((*path, name)))
            _collect(child, (*path, name), found)


def document_paths(text: str) -> set[str]:
    """The paths drawn in the first ```text tree block of `text`, with their groups."""
    parents: dict[int, str] = {}
    paths = [path for line in _tree_lines(text) for path in _line_paths(line, parents)]
    return {prefix for path in paths for prefix in _with_prefixes(path)}


def _line_paths(line: str, parents: dict[int, str]) -> list[str]:
    """The paths of one tree line; `parents` remembers the last path at each depth."""
    match = _CONNECTOR.search(line)
    if not match:
        return []
    depth = match.start() // 4
    paths = _entry_paths(parents.get(depth - 1, ""), line[match.end():])
    parents[depth] = paths[-1]
    return paths


def _tree_lines(text: str) -> list[str]:
    block = re.search(r"```text\n(.*?)```", text, re.S)
    return block.group(1).splitlines() if block else []


def _entry_paths(parent: str, entry: str) -> list[str]:
    """`template show / edit` under `models` is `models template show` and `models template edit`."""
    parts = [_OPTIONAL.sub("", part).split() for part in entry.split(" / ")]
    prefix = parts[0][:-1]
    return [" ".join(filter(None, [parent, *prefix, *words[-1:]])) for words in [parts[0], *parts[1:]]]


def _with_prefixes(path: str) -> list[str]:
    words = path.split()
    return [" ".join(words[:n]) for n in range(1, len(words) + 1)]


def compare(parser: argparse.ArgumentParser, document: Path) -> tuple[list[str], list[str]]:
    """`(undocumented, stale)`: parser paths the document omits, and document paths the parser lacks."""
    real, drawn = parser_paths(parser), document_paths(document.read_text(encoding="utf-8"))
    return sorted(real - drawn), sorted(drawn - real - {_HELP})
