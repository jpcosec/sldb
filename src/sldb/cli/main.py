from __future__ import annotations

import os
import sys
from typing import Any

from sldb.cli.parser import build_parser
from sldb.core.exceptions import SLDBError


_DEPRECATED: dict[str, str] = {
    "store": "stores",
    "model": "models",
    "doc": "docs",
    "ls": "legacy ls",
    "get": "legacy get",
    "glob": "legacy glob",
    "raw-find": "legacy find",
    "recover": "legacy recover",
    "compose": "legacy compose",
}


def _deprecated_handler(old_name: str, replacement: str, handler):
    """Wrap a handler to emit a deprecation warning before delegating."""

    def wrapper(args):
        if not os.environ.get("SLDB_SUPPRESS_DEPRECATION"):
            print(
                f"[deprecated] Use 'sldb {replacement}' instead of 'sldb {old_name}'",
                file=sys.stderr,
            )
        return handler(args)

    return wrapper


class CLI:
    """Main CLI dispatcher for SLDB."""

    def __init__(self):
        from sldb.cli.commands.ast import ASTCLI
        from sldb.cli.commands.basic import BasicCLI
        from sldb.cli.commands.docs import DocsCLI
        from sldb.cli.commands.fields import FieldsCLI
        from sldb.cli.commands.find import FindCLI
        from sldb.cli.commands.help import HelpCLI
        from sldb.cli.commands.init import InitCLI
        from sldb.cli.commands.legacy import LegacyCLI
        from sldb.cli.commands.links import LinkCLI
        from sldb.cli.commands.models import ModelsCLI
        from sldb.cli.commands.query import QueryCLI
        from sldb.cli.commands.sections import SectionsCLI
        from sldb.cli.commands.stores import StoresCLI
        from sldb.cli.commands.store import StoreCLI
        from sldb.cli.commands.model import ModelCLI
        from sldb.cli.commands.doc import DocCLI

        legacy = LegacyCLI()
        query = QueryCLI()
        links = LinkCLI()
        self.handlers = {
            "extract": BasicCLI().extract,
            "render": BasicCLI().render,
            "validate": BasicCLI().validate,
            "init": InitCLI().init,
            "example": InitCLI().example,
            "help": HelpCLI().run,
            "ast": ASTCLI().run,
            "find": FindCLI().run,
            "stores": StoresCLI().run,
            "models": ModelsCLI().run,
            "docs": DocsCLI().run,
            "fields": FieldsCLI().run,
            "sections": SectionsCLI().run,
            "legacy": legacy.run,
            "ls": _deprecated_handler("ls", "legacy ls", query.ls),
            "get": _deprecated_handler("get", "legacy get", query.get),
            "glob": _deprecated_handler("glob", "legacy glob", query.glob),
            "raw-find": _deprecated_handler("raw-find", "legacy find", query.find),
            "recover": _deprecated_handler("recover", "legacy recover", links.recover),
            "compose": _deprecated_handler("compose", "legacy compose", links.compose),
            "store": _deprecated_handler("store", "stores", StoreCLI().run),
            "model": _deprecated_handler("model", "models", ModelCLI().run),
            "doc": _deprecated_handler("doc", "docs", DocCLI().run),
        }

    def run(self, argv: Any = None) -> int:
        parser = build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as e:
            if isinstance(e.code, int):
                return e.code
            return 0 if e.code is None else 1

        command = args.command
        if command != "legacy" and getattr(args, "legacy_query_name", None):
            command = args.legacy_query_name
        handler = self.handlers.get(command)
        if not handler:
            print(f"Unknown command: {command}")
            return 2
        return handler(args)


def main(argv: Any = None) -> int:
    """CLI entry point with error handling."""
    try:
        return CLI().run(argv)
    except SLDBError as e:
        raise SystemExit(str(e))
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Unexpected: {e}")
