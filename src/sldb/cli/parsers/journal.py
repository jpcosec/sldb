"""`sldb journal show|verify`: retired on 2026-11-04; both print where the store's past is read now."""

from __future__ import annotations

import argparse


def add_journal_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("journal", help="Retired (2026-11-04): the store's past is read with `sldb docs history <doc>`.")
    sub = p.add_subparsers(dest="journal_command", required=True)
    _show(sub)
    _verify(sub)


def _show(s: argparse._SubParsersAction) -> None:
    sh = s.add_parser("show", help="Retired: prints the notice and exits 0.")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--limit", type=int, help="Max entries to show")
    sh.add_argument("--since", help="ISO UTC timestamp; only entries at or after it")
    sh.add_argument("--address", help="Only entries for this 'Model:doc' address")
    sh.add_argument("--format", choices=("text", "json", "yaml"), default="text")


def _verify(s: argparse._SubParsersAction) -> None:
    v = s.add_parser("verify", help="Retired: prints the notice and exits 0.")
    v.add_argument("--store", help="Store path")
    v.add_argument("--format", choices=("text", "json", "yaml"), default="text")
