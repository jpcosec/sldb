"""Argument definitions for parser-driven documentation."""
from __future__ import annotations

import argparse


def add_selfdoc_commands(subparsers: argparse._SubParsersAction) -> None:
    """Expose scan, sync, and read-only freshness checks."""
    parser = subparsers.add_parser("selfdoc", help="Derive tracked CLI documentation from a parser.")
    commands = parser.add_subparsers(dest="selfdoc_command", required=True)
    for name, help_text in (("scan", "Inspect parser facts without writing."),
                            ("sync", "Update generated fields and track reference documents."),
                            ("check", "Report documentation drift without writing."),
                            ("python-scan", "Inspect static Python symbols without importing code."),
                            ("python-sync", "Track static Python symbols as reference documents."),
                            ("python-check", "Report static Python documentation drift without writing.")):
        _options(commands.add_parser(name, help=help_text), name)


class _RemovedKgdbFlag(argparse.Action):
    """`--kgdb-command` and `--kgdb-output` served an external kgdb; kgdb is part of sldb now."""

    def __call__(self, parser, namespace, values, option_string=None):
        hint = "use --graph-output" if option_string == "--kgdb-output" else "drop the flag"
        parser.error(f"{option_string} was removed: kgdb is part of sldb and the source graph is written by sldb itself; {hint}")


def _options(parser: argparse.ArgumentParser, command: str) -> None:
    if command.startswith("python-"):
        _python_options(parser)
        if command != "python-scan":
            _output_options(parser)
        return
    _parser_options(parser)
    if command != "scan":
        _output_options(parser)


def _python_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source-root", default="src", help="Python root relative to selected store")
    parser.add_argument("--package", help="Optional package prefix for stable IDs")
    parser.add_argument("--store", help="Store used to anchor source root")
    parser.add_argument("--architecture-spec", help="Explicit spec2viz YAML relative to store root")
    parser.add_argument("--graph-output", default=".sldb/runtime/graphs/python-source.graph.json", help="Source graph (node-link JSON) relative to the store root")
    parser.add_argument("--kgdb-output", action=_RemovedKgdbFlag, help=argparse.SUPPRESS)
    parser.add_argument("--kgdb-command", action=_RemovedKgdbFlag, help=argparse.SUPPRESS)


def _parser_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--factory", default="sldb.cli.parser:build_parser", help="Trusted module:callable returning ArgumentParser")
    parser.add_argument("--pythonpath", help="Import path, relative to the selected project root")
    parser.add_argument("--store", help="Store path or linked alias; otherwise nearest ancestor store")
    parser.add_argument("--include-hidden", action="store_true", help="Include commands/options with suppressed help")


def _output_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--system", default="sldb", help="Stable lowercase tool identifier")
    parser.add_argument("--output", default="knowledge", help="Documentation directory relative to the store root")
