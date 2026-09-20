"""`sldb graph path|cycles|order|components|central|similar` handlers.

Printing wrappers over `sldb.api.graph`'s analysis functions. `--relation` with nothing given
means the authored relations: see `sldb.store.graph.analysis.relations`.
"""

from __future__ import annotations

import json
from typing import Any

from sldb.api.graph import (
    graph_central,
    graph_components,
    graph_cycles,
    graph_islands,
    graph_isolated,
    graph_layers,
    graph_order,
    graph_path,
    graph_paths,
    graph_similar,
)
from sldb.core.exceptions import SLDBError
from sldb.store.graph.analysis import ALL


class GraphAnalysisCLI:
    """The whole-graph questions, as commands."""

    def run(self, args: Any) -> int:
        handlers = {
            "path": self._path,
            "cycles": self._cycles,
            "order": self._order,
            "components": self._components,
            "central": self._central,
            "similar": self._similar,
        }
        return handlers[args.graph_command](args)

    def _path(self, args: Any) -> int:
        if args.all:
            return _print(graph_paths(args.store, args.source, args.target, _rel(args), args.cutoff, args.limit, **_index(args)))
        found = graph_path(args.store, args.source, args.target, _rel(args), args.directed, **_index(args))
        if found is None:
            print(f"No path from {args.source} to {args.target}.")
            return 1
        return _print(found)

    def _cycles(self, args: Any) -> int:
        found = graph_cycles(args.store, _rel(args), args.limit, **_index(args))
        if not found:
            print("No cycles: the relations walked form a DAG.")
            return 0
        return _print(found)

    def _order(self, args: Any) -> int:
        call = graph_layers if args.layers else graph_order
        try:
            return _print(call(args.store, _rel(args), **_index(args)))
        except SLDBError as cyclic:
            print(str(cyclic))
            return 1

    def _components(self, args: Any) -> int:
        if args.isolated:
            return _print(graph_isolated(args.store, _rel(args), _types(args), **_index(args)))
        call = graph_islands if args.islands else graph_components
        return _print(call(args.store, _rel(args), _types(args), **_index(args)))

    def _central(self, args: Any) -> int:
        try:
            ranked = graph_central(args.store, args.kind, _rel(args), _types(args), args.limit, **_index(args))
        except SLDBError as needs_scipy:
            print(str(needs_scipy))
            return 1
        return _print([{"node": node, "score": score} for node, score in ranked])

    def _similar(self, args: Any) -> int:
        ranked = graph_similar(args.store, args.node, _rel(args), args.limit, _types(args), **_index(args))
        return _print([{"node": node, "shared": shared} for node, shared in ranked])


def _rel(args: Any) -> object:
    if args.all_relations and not args.relation:
        return ALL
    return args.relation or _default_relation(args)


def _default_relation(args: Any) -> object:
    return ["tagged_as"] if args.graph_command == "similar" else None


def _types(args: Any) -> object:
    return args.node_type or None


def _index(args: Any) -> dict:
    return {"include_linked": not args.local, "exclude_tags": args.exclude_tag}


def _print(payload: object) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0
