from __future__ import annotations
import argparse

def add_stores_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("stores", help="Store lifecycle and federation.")
    sub = p.add_subparsers(dest="stores_command", required=True)
    _init(sub); _add(sub); _check(sub); _update(sub); _reconcile(sub)
    _semantic_map(sub); _semantic_export(sub); _list(sub)

def _init(s):
    i = s.add_parser("init", help="Init .sldb store.")
    i.add_argument("--path", default=".")
    i.add_argument("--force", action="store_true")

def _add(s):
    a = s.add_parser("add", help="Link federated store.")
    a.add_argument("path", help="Store path")
    a.add_argument("--name", help="Store name")
    a.add_argument("--store", help="Local store path")

def _check(s):
    c = s.add_parser("check", help="Integrity check.")
    c.add_argument("--store", help="Store path")
    c.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    c.add_argument("--pythonpath", help="Project path")

def _update(s):
    u = s.add_parser("update", help="Recompute store hashes.")
    u.add_argument("--wait", action="store_true", help="Wait for store lock if busy")
    u.add_argument("--verbose", action="store_true", help="Print individual skip details")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _reconcile(s):
    r = s.add_parser("reconcile", help="Explicitly reconcile a catalog against a subtree.")
    r.add_argument("--path", default=".", help="Subtree to discover")
    r.add_argument("--catalog", help="Catalog store path; defaults to ~/.sldb")
    r.add_argument("--apply", action="store_true", help="Replace catalog entries with discovered stores")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _semantic_map(s):
    m = s.add_parser("semantic-map", help="Map equivalent semantic concepts.")
    m.add_argument("concept_a", help="First concept")
    m.add_argument("concept_b", help="Second concept")
    m.add_argument("--store", help="Store path")

def _semantic_export(s):
    e = s.add_parser("semantic-export", help="Export semantic payloads.")
    e.add_argument("--store", help="Store path")
    e.add_argument("--pythonpath", help="Project path")
    e.add_argument("--format", choices=("kgdb",), default="kgdb")
    e.add_argument("--encoding", choices=("json", "yaml"), default="json")
    e.add_argument("--output", "-o", default="-", help="Output path or -")
    e.add_argument("--rebuild", action="store_true", help="Refresh semantic and section indexes")

def _list(s):
    l = s.add_parser("list", help="List federated stores.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")
