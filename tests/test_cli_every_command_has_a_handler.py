"""Every top-level command the parser accepts reaches a handler.

The hidden singular groups (`store`, `model`, `doc`) were parsed and shown by `sldb doc --help`
but never registered, so `sldb doc untrack` answered `Unknown command: doc` (graph_ui).
"""

from __future__ import annotations

import argparse

from sldb.cli.dispatcher import CLI
from sldb.cli.parser import build_parser


def test_every_parsed_command_has_a_handler():
    handlers = CLI().handlers
    groups = next(a for a in build_parser()._actions if isinstance(a, argparse._SubParsersAction))
    assert sorted(set(groups.choices) - set(handlers)) == []
