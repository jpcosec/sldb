"""Docs CLI commands module."""
from __future__ import annotations
import json
from typing import Any
import yaml
from sldb.cli.commands.doc import DocCLI
from sldb.cli.commands.docs_exists import docs_exists
from sldb.cli.commands.explore import ExploreCLI
from sldb.cli.commands.links import LinkCLI
from sldb.cli.graph_ops import ast_for_target
from sldb.cli.store_context import get_store_context
from sldb.api.stores.indexed_documents import indexed_documents

class DocsCLI:
    """Plural docs surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._doc = DocCLI()
        self._explore = ExploreCLI()
        self._links = LinkCLI()

    def run(self, args: Any) -> int:
        """Run appropriate docs subcommand.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        cmd = args.docs_command
        if cmd in {"create", "track", "update", "untrack", "delete"}:
            args.doc_command = {"create": "add"}.get(cmd, cmd)
            return self._doc.run(args)
        return self._run_subcommand(cmd, args)

    def _run_subcommand(self, cmd: str, args: Any) -> int:
        handlers = {"list": self.list, "show": self._show, "exists": docs_exists, "recover": self._links.recover, "compose": self._links.compose, "explore": self._explore.run}
        if cmd in handlers:
            return handlers[cmd](args)
        raise SystemExit(f"Unknown docs command: {cmd}")

    def _show(self, args: Any) -> int:
        payload = ast_for_target(args.store, args.pythonpath, f"docs/{args.doc}")
        print(yaml.safe_dump(payload, sort_keys=False) if args.format == "yaml" else json.dumps(payload, indent=2))
        return 0

    def list(self, args: Any) -> int:
        """List tracked documents in the store.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        sp, _root = get_store_context(args.store, mode="readonly")
        docs = indexed_documents(sp)
        return self._render_docs(args.format, {"store": str(sp), "documents": docs}, docs, sp)

    def _render_docs(self, fmt: str, payload: dict[str, Any], docs: list[dict[str, str]], sp: Any) -> int:
        if fmt == "json": print(json.dumps(payload, indent=2))
        elif fmt == "yaml": print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
        elif not docs: print(f"No tracked documents in {sp}")
        else:
            print(f"Tracked documents in {sp}:")
            [print(f"- {i['name']} ({i['model']}) -> {i['path']}") for i in docs]
        return 0
