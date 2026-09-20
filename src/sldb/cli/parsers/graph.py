"""`sldb graph`: query, traverse, analyse and snapshot the store's graph."""

from __future__ import annotations

import argparse

from sldb.cli.parsers.graph_analysis import add_analysis_commands


def add_graph_group(s: argparse._SubParsersAction) -> None:
    """Register `graph get|list|query|neighborhood|path|cycles|order|components|central|similar|snapshot|ingest-sldb`."""
    p = s.add_parser("graph", help="Query, traverse and snapshot the store's graph.")
    sub = p.add_subparsers(dest="graph_command", required=True)
    _add_read_commands(sub)
    add_analysis_commands(sub)
    _add_snapshot(sub)
    _add_ingest(sub)


def _add_read_commands(sub) -> None:
    _add_get(sub)
    _add_list(sub)
    _add_query(sub)
    _add_neighborhood(sub)


def _add_get(sub) -> None:
    p = sub.add_parser("get", help="One node from the store's edge index.")
    p.add_argument("node", help="Node id `sldb://<kind>/...` or export id `Model:name`.")
    _read_args(p)


def _add_list(sub) -> None:
    _read_args(sub.add_parser("list", help="All node ids in the store's edge index."))


def _add_query(sub) -> None:
    p = sub.add_parser("query", help="Run a structured query from a JSON file.")
    p.add_argument("--query-file", required=True, help="Path to a JSON StructuredQuery file.")
    _read_args(p)


def _add_neighborhood(sub) -> None:
    p = sub.add_parser("neighborhood", help="Nodes within a depth of a starting node.")
    p.add_argument("node", help="Starting node id.")
    p.add_argument("--depth", type=int, default=1, help="Hops to traverse (default 1).")
    p.add_argument("--direction", choices=["incoming", "outgoing", "both"], default="both", help="Direction to traverse.")
    _read_args(p)


def _add_snapshot(sub) -> None:
    snap = sub.add_parser("snapshot", help="Save or load the portable graph.")
    inner = snap.add_subparsers(dest="snapshot_command", required=True)
    _add_snapshot_save(inner)
    _add_snapshot_load(inner)


def _add_snapshot_save(inner) -> None:
    p = inner.add_parser("save", help="Export the store's edge index as node-link JSON.")
    p.add_argument("--output", required=True, help="Where to write the node-link JSON.")
    _read_args(p)


def _add_snapshot_load(inner) -> None:
    p = inner.add_parser("load", help="Read a node-link or snapshot JSON file.")
    p.add_argument("--input", required=True, help="The node-link or snapshot JSON file.")


def _add_ingest(sub) -> None:
    p = sub.add_parser("ingest-sldb", help="Convert an sldb semantic export into node-link JSON.")
    p.add_argument("--input", required=True, help="The sldb_kgdb_semantic_export JSON file.")
    p.add_argument("--output", required=True, help="Where to write the node-link JSON.")


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")
