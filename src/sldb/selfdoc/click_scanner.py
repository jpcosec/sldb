"""Introspect an assembled click Group into `CommandRecord` facts, without dispatching
any handler. The same typed facts the argparse `ParserScanner` produces, so a click
CLI can feed the same materialize path.
"""

from __future__ import annotations

import click

from sldb.selfdoc.argument import ArgumentRecord
from sldb.selfdoc.command import CommandRecord
from sldb.selfdoc.values import json_value


def _synopsis(command: click.Command) -> str:
    return command.help or command.short_help or _first_line(command.callback.__doc__)


def _first_line(doc: str | None) -> str:
    return (doc or "").strip().splitlines()[0] if doc and doc.strip() else ""


def _arguments(command: click.Command) -> list[ArgumentRecord]:
    return [_argument(p) for p in command.params]


def _argument(param: click.Parameter) -> ArgumentRecord:
    return ArgumentRecord(
        names=param.opts or [param.name],
        required=bool(param.required or isinstance(param, click.Argument)),
        default=_default(param), choices=_choices(param),
        nargs=None, value_type=_value_type(param),
        action=type(param).__name__, const="", help=param.help or "",
    )


def _default(param: click.Parameter) -> str:
    """The JSON default, or SUPPRESS when the option declares none."""
    if param.default is None or param.default is click.core.UNSET:
        return "SUPPRESS"
    return json_value(param.default)


def _choices(param: click.Parameter) -> list[str] | None:
    values = getattr(getattr(param, "type", None), "choices", None)
    return None if not values else [json_value(v) for v in values]


def _value_type(param: click.Parameter) -> str | None:
    t = getattr(param, "type", None)
    return None if t is None else type(t).__name__


class ClickScanner:
    """Walk a click Group's leaf commands into `CommandRecord` facts."""

    def __init__(self, program: str = "pron") -> None:
        self.program = program

    def scan(self, group: click.Group) -> list[CommandRecord]:
        """One record per leaf command of the group, sorted by name."""
        return [
            self._record(name, command)
            for name, command in sorted(group.commands.items())
            if not isinstance(command, click.Group)
        ]

    def _record(self, name: str, command: click.Command) -> CommandRecord:
        synopsis = _synopsis(command)
        doc = command.callback.__doc__ or ""
        return CommandRecord(
            path=[name], synopsis=synopsis, description=doc.strip(),
            usage=f"{self.program} {name}", group=False, hidden=bool(command.hidden),
            arguments=_arguments(command), exclusive_groups=[],
        )
