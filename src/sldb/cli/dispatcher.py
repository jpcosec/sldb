from __future__ import annotations
from typing import Any
from sldb.cli.parser import build_parser
from sldb.cli.commands.help_texts import SHORT_ARGPARSE_HELP

class CLI:
    def __init__(self):
        self.handlers = {}
        self._load_1()
        self._load_2()
        self._load_3()

    def _load_1(self):
        from sldb.cli.commands.basic import BasicCLI
        from sldb.cli.commands.init import InitCLI
        from sldb.cli.commands.help import HelpCLI
        from sldb.cli.commands.faq import FAQCLI
        from sldb.cli.commands.inbox import InboxCLI
        from sldb.cli.commands.explore import ExploreCLI
        self.handlers.update({"extract": BasicCLI().extract, "render": BasicCLI().render, "validate": BasicCLI().validate})
        self.handlers.update({"init": InitCLI().init, "example": InitCLI().example, "help": HelpCLI().run})
        self.handlers.update({"faq": FAQCLI().run, "inbox": InboxCLI().run, "explore": ExploreCLI().run})

    def _load_2(self):
        from sldb.cli.commands.ast import ASTCLI
        from sldb.cli.commands.find import FindCLI
        from sldb.cli.commands.stores import StoresCLI
        from sldb.cli.commands.models import ModelsCLI
        from sldb.cli.commands.predicates import PredicatesCLI
        from sldb.cli.commands.docs import DocsCLI
        self.handlers.update({"ast": ASTCLI().run, "find": FindCLI().run, "stores": StoresCLI().run})
        self.handlers.update({"models": ModelsCLI().run, "predicates": PredicatesCLI().run, "docs": DocsCLI().run})

    def _load_3(self):
        from sldb.cli.commands.fields import FieldsCLI
        from sldb.cli.commands.sections import SectionsCLI
        from sldb.cli.commands.serve import ServeCLI
        from sldb.cli.commands.lint import lint_cli
        self.handlers.update({"fields": FieldsCLI().run, "sections": SectionsCLI().run})
        self.handlers.update({"serve": ServeCLI().run, "lint": lint_cli})
        self._load_addresses()

    def _load_addresses(self):
        """The raw address surface: `legacy ls|get|glob|find|recover|compose`.

        Addresses are `st.{Model}.doc.field` (structural), `se.tag` (semantic) and
        `gse.tag` (global semantic). The singular top-level aliases (`ls`, `get`,
        `glob`, `raw-find`, `recover`, `compose`) are the pre-redesign spelling and
        route to the same handler.
        """
        from sldb.cli.commands.legacy import LegacyCLI
        legacy = LegacyCLI()
        self.handlers["legacy"] = legacy.run
        for alias in ("ls", "get", "glob", "raw-find", "recover", "compose"):
            self.handlers[alias] = self._alias_to_legacy(legacy, "find" if alias == "raw-find" else alias)

    @staticmethod
    def _alias_to_legacy(legacy, name: str):
        def _run(args):
            args.legacy_command = name
            return legacy.run(args)
        return _run

    def run(self, argv: Any = None) -> int:
        if self._check_help(argv): return 0
        args = self._parse_args(argv)
        if isinstance(args, int): return args
        return self._dispatch(args)

    def _check_help(self, argv: Any) -> bool:
        if argv in (["-h"], ["--help"]): print(SHORT_ARGPARSE_HELP); return True
        return False

    def _parse_args(self, argv: Any) -> Any:
        parser = build_parser()
        try: return parser.parse_args(argv)
        except SystemExit as e: return e.code if isinstance(e.code, int) else (0 if e.code is None else 1)

    def _dispatch(self, args: Any) -> int:
        handler = self.handlers.get(args.command)
        if not handler: print(f"Unknown command: {args.command}"); return 2
        return handler(args)
