"""Write regenerable Python source facts as a node-link graph, with sldb's own graph IO
(`sldb.store.graph`), and tell whether a written one is still current."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def write_source_graph(snapshot: dict, output: Path) -> None:
    """Atomically replace one source graph file (node-link JSON)."""
    from sldb.store.graph.snapshot import GraphSnapshot

    output.parent.mkdir(parents=True, exist_ok=True)
    _replace(GraphSnapshot.model_validate(snapshot), output)


def _replace(graph, output: Path) -> None:
    """Write next to `output`, then rename over it: a reader never sees half a graph."""
    from sldb.store.graph.graph_io import save_graph

    handle, temporary = tempfile.mkstemp(suffix=".json", dir=output.parent)
    os.close(handle)
    try:
        save_graph(graph, temporary)
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)


def graph_is_current(snapshot: dict, output: Path) -> bool:
    """Check that the written graph holds every expected node with its source hash."""
    return graph_state(snapshot, output) == "current"


def graph_state(snapshot: dict, output: Path) -> str:
    """`current`, `stale` (the source moved: an alert), or `missing`/`unreadable` (an error)."""
    if not output.is_file():
        return "missing"
    try:
        nodes = {node["id"]: node["schema"] for node in json.loads(output.read_text(encoding="utf-8"))["nodes"]}
    except (KeyError, TypeError, json.JSONDecodeError):
        return "unreadable"
    expected = {node["identity"]["node_id"]: node for node in snapshot["nodes"]}
    current = set(nodes) == set(expected) and all(_same_source(node, nodes[node_id]) for node_id, node in expected.items())
    return "current" if current else "stale"


def _same_source(expected: dict, actual: dict | None) -> bool:
    if actual is None:
        return False
    return actual.get("source") == expected.get("source") and actual.get("ast") == expected.get("ast")
