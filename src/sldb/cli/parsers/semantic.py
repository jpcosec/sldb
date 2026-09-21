"""`sldb semantic parent add|remove`, `sldb semantic equivalent add`, `sldb semantic show`."""

from __future__ import annotations

import argparse


def add_semantic_group(s: argparse._SubParsersAction) -> None:
    """Register `semantic`: write and read the semantic DAG."""
    p = s.add_parser("semantic", help="Declare what a tag is a kind of, beyond what its name says.")
    sub = p.add_subparsers(dest="semantic_command", required=True)
    _add_parent(sub)
    _add_equivalent(sub)
    _add_show(sub)


def _add_parent(sub) -> None:
    parent = sub.add_parser("parent", help="Add or remove a parent of a tag.")
    inner = parent.add_subparsers(dest="parent_command", required=True)
    for verb, text in (("add", "Declare TAG a kind of PARENT."), ("remove", "Undeclare it.")):
        p = inner.add_parser(verb, help=text)
        p.add_argument("tag", help="The tag, e.g. layer.topology")
        p.add_argument("parent", help="What it is a kind of, e.g. type.knowledge")
        _store_args(p)


def _add_equivalent(sub) -> None:
    eq = sub.add_parser("equivalent", help="Map a local tag to a global one, for gse.")
    inner = eq.add_subparsers(dest="equivalent_command", required=True)
    p = inner.add_parser("add", help="Declare LOCAL equivalent to GLOBAL.")
    p.add_argument("local", help="The tag in this store")
    p.add_argument("global_tag", metavar="global", help="The tag it means across linked stores")
    _store_args(p)


def _add_show(sub) -> None:
    p = sub.add_parser("show", help="A tag's parents, children, and everything above and below it.")
    p.add_argument("tag", help="The tag")
    p.add_argument("--store", help="Store path")


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--actor", help="Who is writing, for the journal")
