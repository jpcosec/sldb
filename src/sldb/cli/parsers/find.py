from __future__ import annotations
import argparse

def add_find_commands(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("find", help="Unified semantic + physical retrieval.", epilog="Typical shapes:\n  sldb find roadmap --in physical --type doc")
    p.add_argument("term", help="Resource term, semantic tag, or physical token")
    p.add_argument("--in", dest="search_in", choices=("semantic", "physical", "both"), default="both", help="Use `physical` for names, paths, section titles, and field addresses")
    for f in ("--global", "--regex", "--fuzzy", "--rebuild"):
        p.add_argument(f, action="store_true", dest="global_scope" if f == "--global" else None)
    p.add_argument("--type", choices=("all", "store", "model", "doc", "section", "field"), default="all")
    p.add_argument("--select", help="Comma-separated projection fields")
    p.add_argument("--where", help="Predicate (docs/architecture/rules-language.md): has(f), f = \"v\", and/or/not, any(depends_on: ...)")
    p.add_argument("--explain", action="store_true", help="With --where: add `findings` (node, holds, clause, seen) for every document evaluated")
    _add_common(p)

def _add_common(p):
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
