"""`sldb graph project` handlers: the project graph as JSON, the payload `GET /project-graph/*` answers too."""

from __future__ import annotations

from typing import Any

from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.cli.output_format import emit


def graph_project(args: Any) -> int:
    """Print the nodes, the edges of one node, or the missing targets; 0 always."""
    graph = project_graph(args.store)
    if args.project_command == "nodes":
        payload = nodes_payload(graph, args.kind)
    elif args.project_command == "edges":
        payload = edges_payload(graph, args.from_id, args.to_id)
    else:
        payload = missing_payload(graph)
    emit(payload, args.format, _text(payload))
    return 0


def nodes_payload(graph: ProjectGraph, kind: str | None) -> dict[str, Any]:
    """`{kind, nodes}`: every document and file node (of `kind`, when given), sorted by id."""
    nodes = [node.to_dict() for node in (*graph.nodes.documents, *graph.nodes.files) if kind is None or node.kind == kind]
    return {"kind": kind, "nodes": sorted(nodes, key=lambda node: node["id"])}


def edges_payload(graph: ProjectGraph, from_id: str | None, to_id: str | None) -> dict[str, Any]:
    """`{from, to, edges}`: the declared edges leaving `from_id` or reaching `to_id`, sorted by key."""
    edges = graph.edges_from(from_id) if from_id is not None else graph.edges_to(to_id or "")
    return {"from": from_id, "to": to_id, "edges": [edge.to_dict() for edge in edges]}


def missing_payload(graph: ProjectGraph) -> dict[str, Any]:
    """`{missing}`: every declared target that resolves to no node, sorted by key."""
    return {"missing": [item.to_dict() for item in graph.extraction().missing_targets]}


def _text(payload: dict[str, Any]) -> str:
    if "nodes" in payload:
        return "\n".join(f"{node['id']} -> {node['path']}" for node in payload["nodes"]) or "No nodes"
    if "edges" in payload:
        return "\n".join(f"{e['source_id']} -{e['role']}-> {e['target_id']} ({e['provenance_path']}:{e['provenance_locator']})" for e in payload["edges"]) or "No edges"
    return "\n".join(f"{m['source_id']} -> {m['target_id']} ({m['provenance_path']}:{m['provenance_locator']}): {m['reason']}" for m in payload["missing"]) or "No missing targets"
