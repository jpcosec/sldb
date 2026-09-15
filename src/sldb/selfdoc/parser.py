"""Introspect assembled argparse trees without dispatching commands."""
from __future__ import annotations

import argparse
from .arguments import arguments, constraints
from .command import CommandRecord


class ParserScanner:
    """Walk nested parser definitions, including inherited argument metadata."""

    def __init__(self, include_hidden: bool = False) -> None:
        self.include_hidden = include_hidden

    def scan(self, parser: argparse.ArgumentParser) -> list[CommandRecord]:
        """Produce deterministic records for every selected command path."""
        return self._walk(parser, [], "", [], [], False)

    def _walk(self, parser, path, synopsis, inherited, groups, hidden):
        own = arguments(parser, self.include_hidden)
        all_arguments, all_groups = inherited + own, groups + constraints(parser)
        subparsers = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
        records = [CommandRecord(path=path, synopsis=synopsis, description=parser.description or "",
                   usage=" ".join(parser.format_usage().split()), group=bool(subparsers), hidden=hidden,
                   arguments=all_arguments, exclusive_groups=all_groups)] if path else []
        for action in subparsers:
            records.extend(self._children(action, path, all_arguments, all_groups, hidden))
        return records

    def _children(self, action, path, inherited, groups, hidden):
        helps = {item.dest: item.help for item in action._choices_actions}
        records = []
        for name, child in sorted(action.choices.items()):
            help_text = helps.get(name, "") or ""
            suppressed = hidden or help_text == argparse.SUPPRESS
            if suppressed and not self.include_hidden:
                continue
            records.extend(self._walk(child, [*path, name], "" if suppressed else help_text,
                                     inherited, groups, suppressed))
        return records
