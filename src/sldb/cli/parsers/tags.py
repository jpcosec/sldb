"""`sldb tags namespaces|tree|check`: the tag namespaces a store declares (docs/architecture/tags.md)."""

from __future__ import annotations

import argparse

from sldb.cli.output_format import add_format


def add_tags_group(s: argparse._SubParsersAction) -> None:
    """Register `tags`: the namespaces of `store.yaml`, one namespace's tree, the checks."""
    p = s.add_parser("tags", help="Tag namespaces: what the store declares, a namespace's tree, and what fails its checks.")
    sub = p.add_subparsers(dest="tags_command", required=True)
    _namespaces(sub)
    _tree(sub)
    _check(sub)


def _namespaces(s) -> None:
    n = s.add_parser("namespaces", help="The declared namespaces: name, hierarchical, folder_axis, anchored_by.")
    _common(n)


def _tree(s) -> None:
    t = s.add_parser("tree", formatter_class=argparse.RawDescriptionHelpFormatter, help="One namespace's tags as a tree: roots (nested by prefix), orphans and unplaced.",
                     epilog="Example:\n  sldb tags tree area --format json")
    t.add_argument("namespace", help="A declared namespace, e.g. area")
    _common(t)


def _check(s) -> None:
    c = s.add_parser("check", help="The findings of builtin:tag_namespace:* over every local document, as `rules check` reports them; exit 1 on an error.")
    _common(c)


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Directory to import models from")
    add_format(p)
