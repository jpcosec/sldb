from __future__ import annotations

import json
from typing import Any

import yaml

from sldb.cli.commands.doc import DocCLI
from sldb.cli.commands.links import LinkCLI
from sldb.cli.graph import ast_for_target


class DocsCLI:
    """Plural docs surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._doc = DocCLI()
        self._links = LinkCLI()

    def run(self, args: Any) -> int:
        command = args.docs_command
        if command in {"create", "track", "update"}:
            args.doc_command = {"create": "add", "track": "track", "update": "update"}[
                command
            ]
            return self._doc.run(args)
        if command == "show":
            payload = ast_for_target(args.store, args.pythonpath, f"docs/{args.doc}")
            if args.format == "yaml":
                print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
            else:
                print(json.dumps(payload, indent=2))
            return 0
        if command == "recover":
            return self._links.recover(args)
        if command == "compose":
            return self._links.compose(args)
        raise SystemExit(f"Unknown docs command: {command}")
