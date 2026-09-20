"""`sldb journal show|verify`: read a store's write journal and verify its hash chain."""

from __future__ import annotations

import argparse


def add_journal_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("journal", help="Read the store's write journal and verify its hash chain.")
    sub = p.add_subparsers(dest="journal_command", required=True)
    _show(sub)
    _verify(sub)


def _show(s: argparse._SubParsersAction) -> None:
    sh = s.add_parser("show", help="Show journal entries, newest first.")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--limit", type=int, help="Max entries to show")
    sh.add_argument("--since", help="ISO UTC timestamp; only entries at or after it")
    sh.add_argument("--address", help="Only entries for this 'Model:doc' address")
    sh.add_argument("--format", choices=("text", "json", "yaml"), default="text")


def _verify(s: argparse._SubParsersAction) -> None:
    v = s.add_parser("verify", help="Verify the journal hash chain.")
    v.add_argument("--store", help="Store path")
    v.add_argument("--format", choices=("text", "json", "yaml"), default="text")
