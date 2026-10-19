"""`sldb edges` handlers: thin printing wrappers over `sldb.api`'s edge index functions."""

from __future__ import annotations

import json
from typing import Any

from sldb.cli.commands.edges_unknown_node import unknown_node_message
from sldb.api import check_edges, edges_from, edges_holding, edges_to, extract_document_payload, init_relations, open_store, rebuild_edges, unresolved_references


class EdgesCLI:
    """Noun-first surface of the edge index."""

    def run(self, args: Any) -> int:
        """Dispatch `edges init|rebuild|show|check|unresolved`; 0 on success, 1 when a check fails."""
        handler = {"init": self._init, "rebuild": self._rebuild, "show": self._show, "check": self._check, "unresolved": self._unresolved}[args.edges_command]
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
        edges = self._edges(args)
        if not edges and (unknown := unknown_node_message(args)):
            raise SystemExit(unknown)
        edges = _with_evidence(args, edges) if args.evidence else edges
        print(json.dumps([e.model_dump() for e in edges], indent=2, ensure_ascii=False))
        return 0

    def _edges(self, args: Any) -> list:
        if args.holds_for:
            subject = extract_document_payload(open_store(args.store, mode="readonly").store_path, args.pythonpath, args.holds_for)
            return edges_holding(args.store, args.node, subject, args.relation, not args.local, args.exclude_tag)
        return (edges_to if args.to else edges_from)(args.store, args.node, args.relation, not args.local, args.exclude_tag)

    def _check(self, args: Any) -> int:
        report = check_edges(args.store, not args.local, args.exclude_tag)
        for line in [f"error: {e}" for e in report.errors] + [f"stale: {s}" for s in report.stale]:
            print(line)
        if report.linked_errors or report.linked_stale:
            print(f"note: linked stores: {len(report.linked_errors)} error(s), {len(report.linked_stale)} stale, theirs to fix (run `edges check` there, or this with --local to leave them out)")
        if report.untracked_builtins:
            print(f"note: builtin relation type(s) not tracked here, checked against sldb's own: {', '.join(report.untracked_builtins)} (`sldb edges init` tracks them)")
        print("Edges OK" if report.ok else f"{len(report.errors)} error(s), {len(report.stale)} stale")
        return 0 if report.ok else 1

    def _unresolved(self, args: Any) -> int:
        """A report, not a check: 0 whatever it finds."""
        found = unresolved_references(args.store, not args.local, args.exclude_tag)
        if args.format == "json":
            print(json.dumps([r.model_dump() for r in found], indent=2, ensure_ascii=False))
            return 0
        for r in found:
            print(f"{r.reason}: {r.source} .{r.field} -> {r.target}" + (f" ({r.target_export_id})" if r.target_export_id else ""))
        print(f"{len(found)} unresolved reference(s)")
        return 0


def _with_evidence(args: Any, edges: list) -> list:
    from sldb.api.edges.edge_evidence import stamp_evidence

    return stamp_evidence(args.store, edges, not args.local)
