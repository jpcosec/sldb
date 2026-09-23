from __future__ import annotations
import argparse
from .docs2 import _add_docs_part2

def add_docs_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("docs", help="Tracked document workflows.", epilog="Note: `recover` and `compose` work on explicit Markdown links and transclusions.")
    sub = p.add_subparsers(dest="docs_command", required=True)
    _create(sub); _track(sub); _update(sub); _untrack(sub); _delete(sub); _show(sub)
    _add_docs_part2(sub)

def _create(s):
    a = s.add_parser("create", help="Create and track document.")
    a.add_argument("--model", required=True)
    a.add_argument("-o", "--output", required=True)
    a.add_argument("payload", help="Data file or inline YAML/JSON")
    a.add_argument("--name", help="Doc name")
    a.add_argument("--store", help="Store path")
    a.add_argument("--pythonpath", help="Project path")

def _track(s):
    t = s.add_parser("track", help="Track existing doc.")
    t.add_argument("path", help="Document path")
    t.add_argument("--model", required=True)
    t.add_argument("--name", help="Doc name")
    t.add_argument("--store", help="Store path")
    t.add_argument("--pythonpath", help="Project path")
    t.add_argument("--force", action="store_true")

def _update(s):
    u = s.add_parser("update", help="Update doc content.")
    u.add_argument("doc", help="Doc name or path")
    u.add_argument("payload", help="Data file or inline YAML/JSON")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _untrack(s):
    rm = s.add_parser("untrack", help="Remove a tracked doc from the store, keeping its file.")
    rm.add_argument("doc", help="Doc name or tracked path")
    rm.add_argument("--store", help="Store path")
    rm.add_argument("--pythonpath", help="Project path")

def _delete(s):
    d = s.add_parser("delete", help="Untrack a doc AND delete its Markdown file.")
    d.add_argument("doc", help="Doc name or tracked path")
    d.add_argument("--store", help="Store path")
    d.add_argument("--pythonpath", help="Project path")
    d.add_argument("--yes", action="store_true", help="Do not ask for confirmation")

def _show(s):
    sh = s.add_parser("show", help="Show document AST and payload.")
    sh.add_argument("doc", help="Doc name or Model/DocName or tracked path")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--pythonpath", help="Project path")
    sh.add_argument("--format", choices=("json", "yaml"), default="json")
