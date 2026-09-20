"""`sldb graph path|cycles|order|components|central|similar`: the whole-graph questions."""

from __future__ import annotations

import argparse

from sldb.store.graph.analysis import KINDS


def add_analysis_commands(sub) -> None:
    """Register the six analysis subcommands under `sldb graph`."""
    _add_path(sub)
    _add_cycles(sub)
    _add_order(sub)
    _add_components(sub)
    _add_central(sub)
    _add_similar(sub)


def _add_path(sub) -> None:
    p = sub.add_parser("path", help="How two nodes are connected.")
    p.add_argument("source", help="Node id to start from.")
    p.add_argument("target", help="Node id to reach.")
    p.add_argument("--directed", action="store_true", help="Follow edges only the way they point")
    p.add_argument("--all", action="store_true", help="Every route, not just the shortest")
    p.add_argument("--cutoff", type=int, help="With --all, the longest route to consider, in hops")
    p.add_argument("--limit", type=int, default=10, help="With --all, how many routes to print (default 10)")
    _walk_args(p)


def _add_cycles(sub) -> None:
    p = sub.add_parser("cycles", help="Cycles in a relation that should be a DAG.")
    p.add_argument("--limit", type=int, default=10, help="How many cycles to print (default 10)")
    _walk_args(p)


def _add_order(sub) -> None:
    p = sub.add_parser("order", help="The nodes in dependency order.")
    p.add_argument("--layers", action="store_true", help="Group the order into levels")
    _walk_args(p)


def _add_components(sub) -> None:
    p = sub.add_parser("components", help="What hangs together, and what hangs alone.")
    p.add_argument("--islands", action="store_true", help="Only the groups outside the largest one")
    p.add_argument("--isolated", action="store_true", help="Only the nodes with no edge at all")
    _walk_args(p)


def _add_central(sub) -> None:
    p = sub.add_parser("central", help="Which nodes the rest of the store leans on.")
    p.add_argument("--kind", choices=list(KINDS), default="pagerank", help="How to measure (default pagerank)")
    p.add_argument("--limit", type=int, default=20, help="How many nodes to print (default 20)")
    _walk_args(p)


def _add_similar(sub) -> None:
    p = sub.add_parser("similar", help="Which nodes resemble this one, by shared targets.")
    p.add_argument("node", help="Node id to compare against.")
    p.add_argument("--limit", type=int, default=10, help="How many nodes to print (default 10)")
    _walk_args(p, default_relation="tagged_as")


def _walk_args(p: argparse.ArgumentParser, default_relation: str | None = None) -> None:
    hint = f" (default {default_relation})" if default_relation else " (default: the authored ones)"
    p.add_argument("--relation", action="append", default=[], help=f"Relation to walk, repeatable{hint}")
    p.add_argument("--all-relations", action="store_true", help="Walk every relation, derived spine included")
    p.add_argument("--type", action="append", default=[], dest="node_type", help="Keep only nodes of this class, repeatable")
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")
