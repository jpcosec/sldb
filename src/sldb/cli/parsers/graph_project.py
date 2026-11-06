"""`sldb graph project nodes|edges|missing`: the project graph the store declares in `store.yaml`."""

from __future__ import annotations

import argparse

from sldb.cli.output_format import add_format


def add_project_commands(sub: argparse._SubParsersAction) -> None:
    """Register `graph project nodes [--kind K] | edges --from ID | --to ID | missing`."""
    p = sub.add_parser("project", help="The project graph declared under project_graph in store.yaml: documents, files and declared edges.")
    inner = p.add_subparsers(dest="project_command", required=True)
    nodes = inner.add_parser("nodes", help="Every document and file node, sorted by id.")
    nodes.add_argument("--kind", help="Only nodes of this kind")
    _read_args(nodes)
    _add_edges(inner)
    _read_args(inner.add_parser("missing", help="Declared targets that resolve to no node, with where each is declared."))


def _add_edges(inner: argparse._SubParsersAction) -> None:
    edges = inner.add_parser("edges", help="Declared edges leaving (--from) or reaching (--to) a node, with their provenance.")
    ends = edges.add_mutually_exclusive_group(required=True)
    ends.add_argument("--from", dest="from_id", metavar="ID", help="Edges leaving this node id")
    ends.add_argument("--to", dest="to_id", metavar="ID", help="Edges reaching this node id")
    _read_args(edges)


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    add_format(p)
