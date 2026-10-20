"""`sldb anchors`: anchors to code, recorded and checked (docs/architecture/code-anchoring.md)."""

from __future__ import annotations

import argparse


def add_anchors_group(s: argparse._SubParsersAction) -> None:
    """Register `anchors record|check`."""
    p = s.add_parser("anchors", help="Anchors to code: what a symbol looked like, and whether it still does.")
    sub = p.add_subparsers(dest="anchors_command", required=True)
    _record(sub)
    _check(sub)


def _record(sub: argparse._SubParsersAction) -> None:
    r = sub.add_parser("record", help="What the symbol looks like now: the block an anchor keeps (code:<path>::<name>).", epilog="Example:\n  sldb anchors record code:src/sldb/cli/main.py::main --write knowledge/anchors/main.md --claim 'the entry point'")
    r.add_argument("ref", help="code:<path>::<qualified_name>; an empty name is the module")
    r.add_argument("--write", metavar="PATH", help="Create (or re-record) a CodeAnchorDoc at this path, tracked in the store")
    r.add_argument("--claim", default="", help="With --write: what is being said because of this symbol")
    r.add_argument("--name", help="With --write: document name (default: the file stem)")
    r.add_argument("--store", help="Store path")
    r.add_argument("--pythonpath", help="Project path")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="yaml")


def _check(sub: argparse._SubParsersAction) -> None:
    c = sub.add_parser("check", help="Every anchor of the store against the code now; reads only, unless --record.", epilog="Exit 0 with alerts only (changed, reconnected, lost, renormalize); 1 on an error (unparseable, invalid, unavailable).")
    c.add_argument("--record", action="store_true", help="Write the reconnections into the anchors (new ref, a history entry); the only write")
    c.add_argument("--store", help="Store path")
    c.add_argument("--pythonpath", help="Project path")
    c.add_argument("--format", choices=("text", "json", "yaml"), default="text")
