"""`sldb edges` handlers: thin printing wrappers over `sldb.api`'s edge index functions."""

from __future__ import annotations

import json
from typing import Any

from sldb.api import check_edges, edges_from, edges_holding, edges_to, extract_document_payload, init_relations, open_store, rebuild_edges


class EdgesCLI:
    """Noun-first surface of the edge index."""

    def run(self, args: Any) -> int:
        """Dispatch `edges init|rebuild|show|check`; 0 on success, 1 when a check fails."""
        handler = {"init": self._init, "rebuild": self._rebuild, "show": self._show, "check": self._check}[args.edges_command]
        return handler(args)

    def _init(self, args: Any) -> int:
        print(f"Initialized relations: {init_relations(args.store, args.pythonpath).summary()}")
        return 0

    def _rebuild(self, args: Any) -> int:
        report = rebuild_edges(args.store, args.pythonpath)
        print(f"Edges: {report.docs_written} shard(s) written, {report.docs_reused} reused, {report.models_walked} model(s) walked")
        return 0

    def _show(self, args: Any) -> int:
        if args.holds_for and args.to:
            raise SystemExit("--holds-for reads the edges leaving the node; it does not combine with --to")
        if args.holds_for:
            subject = extract_document_payload(open_store(args.store, mode="readonly").store_path, args.pythonpath, args.holds_for)
            edges = edges_holding(args.store, args.node, subject, args.relation, not args.local, args.exclude_tag)
        else:
            edges = (edges_to if args.to else edges_from)(args.store, args.node, args.relation, not args.local, args.exclude_tag)
        print(json.dumps([e.model_dump() for e in edges], indent=2, ensure_ascii=False))
        return 0

    def _check(self, args: Any) -> int:
        report = check_edges(args.store, not args.local, args.exclude_tag)
        for line in [f"error: {e}" for e in report.errors] + [f"stale: {s}" for s in report.stale]:
            print(line)
        if report.untracked_builtins:
            print(f"note: builtin relation type(s) not tracked here, checked against sldb's own: {', '.join(report.untracked_builtins)} (`sldb edges init` tracks them)")
        print("Edges OK" if report.ok else f"{len(report.errors)} error(s), {len(report.stale)} stale")
        return 0 if report.ok else 1
