"""`sldb graph` handlers: thin printing wrappers over `sldb.api`'s graph functions."""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from sldb.api.graph import (
    collect_neighborhood,
    collect_neighborhood_by_direction,
    execute_query,
    graph_get,
    graph_list,
    ingest_sldb,
    save_graph,
    snapshot_load,
    snapshot_save,
)
from sldb.cli import alert_sink
from sldb.cli.commands.graph_analysis import GraphAnalysisCLI
from sldb.core.finding import Finding
from sldb.store.graph.language import StructuredQuery


class GraphCLI:
    """Noun-first surface of the graph layer."""

    def __init__(self, backend: Any = None) -> None:
        self.backend = backend

    def run(self, args: Any) -> int:
        handlers = {
            "get": self._get,
            "list": self._list,
            "query": self._query,
            "neighborhood": self._neighborhood,
            "snapshot": self._snapshot,
            "ingest-sldb": self._ingest_sldb,
        }
        handler = handlers.get(args.graph_command)
        return handler(args) if handler else GraphAnalysisCLI(backend=self.backend).run(args)

    def _get(self, args: Any) -> int:
        node = graph_get(args.store, args.node, not args.local, args.exclude_tag)
        if node is None:
            return 1
        print(json.dumps(node.model_dump(), indent=2, ensure_ascii=False))
        return 0

    def _list(self, args: Any) -> int:
        print(json.dumps(graph_list(args.store, not args.local, args.exclude_tag), indent=2, ensure_ascii=False))
        return 0

    def _query(self, args: Any) -> int:
        with warnings.catch_warnings():  # the deprecation travels in the envelope's warnings
            warnings.simplefilter("ignore", DeprecationWarning)
            query = StructuredQuery.model_validate(json.loads(Path(args.query_file).read_text(encoding="utf-8")))
        _warn_field_conditions(query)
        nodes = execute_query(args.store, query, not args.local, args.exclude_tag)
        print(json.dumps([n.model_dump() for n in nodes], indent=2, ensure_ascii=False))
        return 0

    def _neighborhood(self, args: Any) -> int:
        if args.direction == "both":
            ids = collect_neighborhood(args.store, [args.node], args.depth, not args.local, args.exclude_tag)
        else:
            ids = collect_neighborhood_by_direction(args.store, {args.node}, args.depth, args.direction, not args.local, args.exclude_tag)
        print(json.dumps(sorted(ids), indent=2, ensure_ascii=False))
        return 0

    def _snapshot(self, args: Any) -> int:
        return {"save": self._snapshot_save, "load": self._snapshot_load}[args.snapshot_command](args)

    def _snapshot_save(self, args: Any) -> int:
        snapshot_save(args.store, args.output, not args.local, args.exclude_tag)
        print(f"Saved graph snapshot to {args.output}")
        return 0

    def _snapshot_load(self, args: Any) -> int:
        print(json.dumps(snapshot_load(args.input).model_dump(mode="json"), indent=2, ensure_ascii=False))
        return 0

    def _ingest_sldb(self, args: Any) -> int:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        save_graph(ingest_sldb(payload), args.output)
        print(f"Saved graph snapshot to {args.output}")
        return 0


def _warn_field_conditions(query: StructuredQuery) -> None:
    """A query with `FieldCondition` filters reports the deprecation (GO05 p1, p12): one
    `warning` in the envelope naming the predicate that replaces them; the output is unchanged."""
    predicates = [c.predicate().text for f in query.filters for c in f.conditions]
    if not predicates:
        return
    what = "FieldCondition is deprecated; write the predicate instead: " + " and ".join(predicates)
    alert_sink.report([Finding("warning", "deprecated/field-condition", "graph query", what, "docs/architecture/rules-language.md")], text=False)
