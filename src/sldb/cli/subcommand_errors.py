"""An unknown argument is reported by the subcommand that rejected it, with its own usage.

`parse_args` on the root parser reports leftovers from the root, so `models show X --format
json` printed the whole `sldb` usage and said nothing about which command refused the flag.
"""

from __future__ import annotations

import argparse
from typing import Any


def parse_reporting_subcommand(parser: argparse.ArgumentParser, argv: Any) -> argparse.Namespace:
    args, extras = parser.parse_known_args(argv)
    if extras:
        _deepest(parser, args).error(f"unrecognized arguments: {' '.join(extras)}")
    return args


def _deepest(parser: argparse.ArgumentParser, args: argparse.Namespace) -> argparse.ArgumentParser:
    """The last subparser `args` went through: follow each chosen subcommand down."""
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction) and (chosen := getattr(args, action.dest, None)) in action.choices:
            return _deepest(action.choices[chosen], args)
    return parser
