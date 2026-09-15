from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.commands.explore_hit import ExploreHit
from sldb.cli.commands.explore_docs import ExploreDocs
from sldb.cli.commands.explore_code import ExploreCode
from sldb.cli.store_context import get_store_context


class ExploreCLI:
    """Search repo docs and Python docstrings."""

    def run(self, args: Any) -> int:
        hits = self._gather_hits(args)[: args.max_results]
        payload = [asdict(hit) for hit in hits]
        self._print_results(payload, args.format)
        return 0 if payload else 1

    def _gather_hits(self, args: Any) -> list[ExploreHit]:
        root = self._project_root(args)
        hits: list[ExploreHit] = []
        if args.source in {"all", "docs"}:
            hits.extend(ExploreDocs().search(args.term, self._resolve_root(root, args.docs_root), args.regex))
        if args.source in {"all", "docstrings"}:
            hits.extend(ExploreCode().search(args.term, self._resolve_root(root, args.code_root), args.regex))
        return hits

    def _project_root(self, args: Any) -> Path:
        if self._has_absolute_roots(args) and not getattr(args, "store", None):
            return Path.cwd()
        _store, root = get_store_context(getattr(args, "store", None), mode="readonly")
        return root

    def _has_absolute_roots(self, args: Any) -> bool:
        return Path(args.docs_root).is_absolute() and Path(args.code_root).is_absolute()

    def _resolve_root(self, root: Path, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else root / path

    def _print_results(self, payload: list[dict[str, Any]], format_type: str) -> None:
        if format_type == "json":
            print(json.dumps({"results": payload}, indent=2))
        elif format_type == "yaml":
            print(yaml.safe_dump({"results": payload}, sort_keys=False, allow_unicode=True))
        else:
            for hit in payload:
                print(self._format_text(hit))

    def _format_text(self, hit: dict[str, Any]) -> str:
        return (
            f"{hit['source']}:{hit['kind']} | {hit['path']}:{hit['line']} | "
            f"{hit['anchor']} | {hit['snippet']}"
        )
