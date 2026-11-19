"""Extract argument and group metadata from argparse."""
from __future__ import annotations

import argparse
from .argument import ArgumentRecord
from .constraint import ExclusiveGroup
from .values import json_value, qualified_name


def _required(action: argparse.Action) -> bool:
    """Return `required` independent of the Python patch version.

    Older 3.12 patch releases mark a defaultless `nargs="*"` positional as required, newer ones
    do not. Normalize to the historical rule so generated references are stable.
    """
    if not action.option_strings and action.nargs == argparse.ZERO_OR_MORE and action.default is None:
        return True
    return bool(action.required)


def argument_record(action: argparse.Action) -> ArgumentRecord:
    """Keep parser constraints, defaults, and help in a typed record."""
    return ArgumentRecord(
        names=action.option_strings or [action.dest], required=_required(action),
        default="SUPPRESS" if action.default == argparse.SUPPRESS else json_value(action.default),
        choices=None if action.choices is None else [json_value(v) for v in action.choices],
        nargs=action.nargs, value_type=qualified_name(action.type) if callable(action.type) else action.type,
        action=qualified_name(type(action)), const=json_value(action.const), help=action.help or "",
    )


def arguments(parser: argparse.ArgumentParser, include_hidden: bool) -> list[ArgumentRecord]:
    """Return ordinary arguments, excluding subparser dispatch and built-in help."""
    return [argument_record(a) for a in parser._actions
            if not isinstance(a, (argparse._SubParsersAction, argparse._HelpAction))
            and (include_hidden or a.help != argparse.SUPPRESS)]


def constraints(parser: argparse.ArgumentParser) -> list[ExclusiveGroup]:
    """Retain required mutually exclusive selections."""
    return [ExclusiveGroup(required=g.required, arguments=[a.dest for a in g._group_actions])
            for g in parser._mutually_exclusive_groups]
