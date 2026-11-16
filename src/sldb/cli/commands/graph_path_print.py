"""`sldb graph path` handler: the route (or routes) between two nodes, explained on demand.

With `--explain` each route prints as `{"path", "steps"}`, every step with the edges joining
its two nodes (relation, direction walked, provenance): see
`sldb.store.graph.analysis.path_steps`. Without it the output is the list of ids, as always.
"""

from __future__ import annotations

import json
from typing import Any

from sldb.api.graph import graph_path, graph_paths


def print_path(args: Any, backend: Any, relations: object, index: dict) -> int:
    """Print the shortest route, or with `--all` up to `--limit` routes; 1 when there is none."""
    if args.all:
        return _print(graph_paths(args.store, args.source, args.target, relations, args.cutoff, args.limit, backend=backend, explain=args.explain, **index))
    found = graph_path(args.store, args.source, args.target, relations, args.directed, backend=backend, explain=args.explain, **index)
    if found is None:
        print(f"No path from {args.source} to {args.target}.")
        return 1
    return _print(found)


def _print(payload: object) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0
