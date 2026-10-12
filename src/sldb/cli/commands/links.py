from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.store_context import get_store_context
from sldb.cli.commands.links_all import batch_requested, recover_all
from sldb.cli.utils import write_text
from sldb.links import compose_document, recover_links, resolve_document_input


class LinkCLI:
    """Handles link recovery and document composition."""

    def recover(self, args: Any) -> int:
        if batch_requested(args): return recover_all(args)
        sp, root = get_store_context(args.store)
        res = recover_links(
            resolve_document_input(args.doc, sp), sp,
            include_transclusions=args.include_transclusions, depth=args.depth,
        )
        if args.links_only:
            return self._print_links_only(res)
        self._print_recovery(res, args.format)
        return 0 if not res.get("unresolved") else 1

    def _print_links_only(self, res: dict) -> int:
        targets = sorted(set(link["target"] for link in res.get("links", [])))
        for t in targets:
            print(t)
        return 0 if not res.get("unresolved") else 1

    def _print_recovery(self, res: dict, fmt: str) -> None:
        if fmt == "text":
            for link in res.get("links", []):
                self._print_link_text(link)
        elif fmt == "json":
            print(json.dumps(res, indent=2))
        else:
            print(yaml.dump(res, allow_unicode=True, sort_keys=False))

    def _print_link_text(self, link: dict) -> None:
        resolved = "ok" if link["resolved"] else "FAIL"
        if link.get("predicate"):
            w5h1 = f"[{link['w5h1_type']}]" if link.get("w5h1_type") else ""
            print(f"{link['kind']}: [{link['predicate']}]{w5h1} {link['target']} [{resolved}]")
        else:
            print(f"{link['kind']}: {link['target']} [{resolved}]")

    def compose(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        doc = resolve_document_input(args.doc, sp)
        res = compose_document(doc, sp, links_base=self._links_base(args, doc))
        self._write_composed(args, res)
        return 0 if not res["unresolved"] else 1

    @staticmethod
    def _links_base(args: Any, doc: Path) -> Path | None:
        if not args.render_links: return None
        return doc.parent if args.output == "-" else Path(args.output).resolve().parent

    def _write_composed(self, args: Any, res: dict) -> None:
        if args.format == "markdown":
            write_text(args.output, res["markdown"] + "\n")
        elif args.format == "yaml":
            write_text(args.output, yaml.safe_dump(res, sort_keys=False, allow_unicode=True))
        else:
            write_text(args.output, json.dumps(res, indent=2))
