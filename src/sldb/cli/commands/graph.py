"""`sldb graph` handlers: thin printing wrappers over `sldb.api`'s graph functions."""

from __future__ import annotations

import json
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
from sldb.store.graph.language import StructuredQuery


class GraphCLI:
    """Noun-first surface of the graph layer."""

    def run(self, args: Any) -> int:
        handlers = {
            "get": self._get,
            "list": self._list,
            "query": self._query,
            "neighborhood": self._neighborhood,
            "snapshot": self._snapshot,
            "ingest-sldb": self._ingest_sldb,
        }
        return handlers[args.graph_command](args)

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
        query = StructuredQuery.model_validate(json.loads(Path(args.query_file).read_text(encoding="utf-8")))
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
