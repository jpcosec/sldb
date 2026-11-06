"""`sldb edges`: the edge index (typed nodes and edges of the store) from the command line."""

from __future__ import annotations

import argparse

from sldb.cli.output_format import add_format


def add_edges_group(s: argparse._SubParsersAction) -> None:
    """Register `edges init|rebuild|show|check|unresolved|referrers|rewrite`."""
    p = s.add_parser("edges", help="Typed nodes and edges of the store (the edge index).")
    sub = p.add_subparsers(dest="edges_command", required=True)
    _store_args(sub.add_parser("init", help="Register RelationTypeDoc/RelationDoc and track the builtin relation types."))
    _store_args(sub.add_parser("rebuild", help="Bring the edge index current; only what moved is rewritten."))
    _read_args(sub.add_parser("check", help="Validate every edge against its relation type."))
    _show_args(sub.add_parser("show", help="Edges from (or --to) a document or node."))
    unresolved = sub.add_parser("unresolved", help="Declared references that name no document.")
    unresolved.add_argument("--format", choices=("text", "json"), default="text")
    _read_args(unresolved)
    _reference_commands(sub)


def _reference_commands(sub: argparse._SubParsersAction) -> None:
    """`edges referrers TARGET` and `edges rewrite TARGET --to NEW | --remove [--dry-run]` (GD22)."""
    referrers = sub.add_parser("referrers", help="Every reference to a document or project node: declared fields (scalar or list element) and mentions in prose.")
    referrers.add_argument("target", help="Doc name, Model/name, Model:name, tracked path, or a project graph node id (kind:identity)")
    _store_args(referrers)
    add_format(referrers)
    _rewrite_args(sub.add_parser("rewrite", help="Rewrite (--to) or remove (--remove) every reference to a document or project node, all or nothing."))


def _rewrite_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("target", help="As in `edges referrers`")
    what = p.add_mutually_exclusive_group(required=True)
    what.add_argument("--to", metavar="NEW", help="The replacement: resolved like TARGET (each value keeps its form), else written as given")
    what.add_argument("--remove", action="store_true", help="Remove the references: a scalar field becomes null, a list loses the element, a mention is reported as skipped")
    p.add_argument("--dry-run", dest="dry_run", action="store_true", help="Report what would change, validated in memory, without writing")
    _store_args(p)
    add_format(p)


def _show_args(show: argparse.ArgumentParser) -> None:
    show.add_argument("node", help="Export id `Model:name`, or a node id `sldb://<kind>/...`")
    show.add_argument("--to", action="store_true", help="Edges pointing at the node instead of leaving it")
    show.add_argument("--relation", help="Only edges of this relation type")
    show.add_argument("--holds-for", metavar="DOC", help="Only edges whose condition holds on this document's fields (name, path or Model/name)")
    show.add_argument("--pythonpath", help="Project path (to read the --holds-for document)")
    show.add_argument("--evidence", action="store_true", help="Add metadata.evidence: the target's hash, the source's contract, and the engine or actor")
    _read_args(show)


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")
