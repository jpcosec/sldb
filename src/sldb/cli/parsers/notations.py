"""`sldb notations`: Visual notations, palettes, views, and resolving from the command line."""

from __future__ import annotations

import argparse


def add_notations_group(s: argparse._SubParsersAction) -> None:
    """Register `notations list|sync|view|resolve`."""
    p = s.add_parser("notations", help="Visual notations, palettes, views and diagram resolver.")
    sub = p.add_subparsers(dest="notations_command", required=True)

    # list
    p_list = sub.add_parser("list", help="List notations or projection views in the store or builtins.")
    p_list.add_argument("--views", action="store_true", help="List projection views instead of notations")
    _store_args(p_list)

    # sync
    p_sync = sub.add_parser("sync", help="Synchronize a notation or palette into the store.")
    p_sync.add_argument("--notation", help="Notation name or YAML file to sync")
    p_sync.add_argument("--palette", help="Palette name or YAML file to sync")
    _store_args(p_sync)

    # view
    p_view = sub.add_parser("view", help="Resolve a SpecDoc or projection view.")
    p_view.add_argument("spec", help="SpecDoc reference (e.g. SpecDoc:arch or arch) or ViewDoc reference")
    p_view.add_argument("--projection", action="store_true", help="Evaluate as projection view instead of SpecDoc")
    _store_args(p_view)

    # resolve
    p_resolve = sub.add_parser("resolve", help="Resolve documents under a notation without a SpecDoc.")
    p_resolve.add_argument("--notation", required=True, help="NotationDoc reference (e.g. NotationDoc:uml-class or uml-class)")
    p_resolve.add_argument("--docs", nargs="+", required=True, help="Document references to style (Model:name)")
    p_resolve.add_argument("--relations", nargs="*", help="Optional RelationDoc references to style")
    _store_args(p_resolve)


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")
