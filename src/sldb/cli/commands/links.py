from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.cli.utils import get_store_context, write_text
from sldb.links import recover_links, compose_document


class LinkCLI:
    """Handles link recovery and document composition."""

    def recover(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        res = recover_links(
            Path(args.doc).resolve(),
            sp,
            include_transclusions=args.include_transclusions,
            depth=args.depth,
        )

        if args.links_only:
            targets = sorted(set(link["target"] for link in res.get("links", [])))
            for t in targets:
                print(t)
            return 0 if not res.get("unresolved") else 1

        if args.format == "text":
            for link in res.get("links", []):
                print(
                    f"{link['kind']}: {link['target']} [{'ok' if link['resolved'] else 'FAIL'}]"
                )
        elif args.format == "json":
            print(json.dumps(res, indent=2))
        else:
            import yaml

            print(yaml.dump(res, allow_unicode=True, sort_keys=False))

        return 0 if not res.get("unresolved") else 1

    def compose(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        res = compose_document(Path(args.doc).resolve(), sp)
        if args.format == "markdown":
            write_text(args.output, res["markdown"] + "\n")
        else:
            write_text(args.output, json.dumps(res, indent=2))
        return 0 if not res["unresolved"] else 1
