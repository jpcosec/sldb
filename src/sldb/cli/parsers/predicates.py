from __future__ import annotations
import argparse

def add_predicates_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("predicates", help="Store-backed semantic link predicates.")
    sub = p.add_subparsers(dest="predicates_command", required=True)
    _add(sub); _list(sub); _show(sub); _validate(sub); _remove(sub); _sync(sub); _export(sub)

def _add(s):
    a = s.add_parser("add", help="Register a predicate definition.")
    a.add_argument("name", help="Predicate name used in [name:: [[target]]].")
    a.add_argument("--axis", required=True, help="Semantic axis, for example HOW.")
    a.add_argument("--description", default="", help="Predicate description.")
    a.add_argument("--store", help="Store path")

def _list(s):
    l = s.add_parser("list", help="List predicate definitions.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _show(s):
    sh = s.add_parser("show", help="Show one predicate definition.")
    sh.add_argument("name", help="Predicate name")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _validate(s):
    v = s.add_parser("validate", help="Validate predicate definitions.")
    v.add_argument("name", nargs="?", help="Optional predicate name")
    v.add_argument("--store", help="Store path")
    v.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _remove(s):
    r = s.add_parser("remove", help="Remove a predicate definition.")
    r.add_argument("name", help="Predicate name")
    r.add_argument("--store", help="Store path")

def _sync(s):
    y = s.add_parser("sync", help="Make the store match a versioned predicates file (create/update; --prune removes the rest).", epilog="File format:\n  is_solved_by: {axis: HOW, description: ...}")
    y.add_argument("--file", required=True, help="YAML file: name -> {axis, description}; - for stdin")
    y.add_argument("--prune", action="store_true", help="Remove store predicates absent from the file")
    y.add_argument("--store", help="Store path")

def _export(s):
    x = s.add_parser("export", help="Write the store predicates to a YAML file (input of `predicates sync`).")
    x.add_argument("--file", default="-", help="Output file, - for stdout")
    x.add_argument("--store", help="Store path")
