"""`sldb edges`: the edge index (typed nodes and edges of the store) from the command line."""

from __future__ import annotations

import argparse


def add_edges_group(s: argparse._SubParsersAction) -> None:
    """Register `edges init|rebuild|show|check`."""
    p = s.add_parser("edges", help="Typed nodes and edges of the store (the edge index).")
    sub = p.add_subparsers(dest="edges_command", required=True)
    _store_args(sub.add_parser("init", help="Register RelationTypeDoc/RelationDoc and track the builtin relation types."))
    _store_args(sub.add_parser("rebuild", help="Bring the edge index current; only what moved is rewritten."))
    _read_args(sub.add_parser("check", help="Validate every edge against its relation type."))
    show = sub.add_parser("show", help="Edges from (or --to) a document or node.")
    show.add_argument("node", help="Export id `Model:name`, or a node id `sldb://<kind>/...`")
    show.add_argument("--to", action="store_true", help="Edges pointing at the node instead of leaving it")
    show.add_argument("--relation", help="Only edges of this relation type")
    _read_args(show)


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")
