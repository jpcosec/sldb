"""Node-link JSON read/write for the portable graph, without networkx."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.store.graph.node import KnowledgeNode
from sldb.store.graph.snapshot import GraphSnapshot


def save_graph(snapshot: GraphSnapshot, path: str | Path) -> None:
    """Write a snapshot as node-link JSON, in the on-disk format kgdb consumers read."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_node_link(snapshot), indent=2, ensure_ascii=False), encoding="utf-8")


def load_graph(path: str | Path) -> GraphSnapshot:
    """Read node-link JSON (or a native snapshot) back into a GraphSnapshot."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "nodes" in data and "links" not in data and "edges" not in data:
        return GraphSnapshot.model_validate(data)
    return _snapshot_from_node_link(data)


def _node_link(snapshot: GraphSnapshot) -> dict:
    nodes = [_node_entry(n) for n in snapshot.nodes]
    links = [_link_entry(n.identity.node_id, e) for n in snapshot.nodes for e in n.edges]
    return {"directed": True, "multigraph": False, "graph": {}, "nodes": nodes, "links": links}


def _node_entry(node: KnowledgeNode) -> dict:
    return {"type": node.identity.node_type, "status": _status(node), "schema": node.model_dump(), "id": node.identity.node_id}


def _status(node: KnowledgeNode) -> str:
    return node.compliance.status if node.compliance else "unknown"


def _link_entry(source: str, edge) -> dict:
    return {"relation": edge.relation_type, "metadata": edge.metadata, "source": source, "target": edge.target_id}


def _snapshot_from_node_link(data: dict) -> GraphSnapshot:
    nodes = [_node_from_entry(e) for e in data["nodes"]]
    return GraphSnapshot(version="1.0", nodes=nodes, metadata={})


def _node_from_entry(entry: dict) -> KnowledgeNode:
    schema = entry.get("schema")
    if schema:
        return KnowledgeNode.model_validate(schema)
    return KnowledgeNode.model_validate({"identity": {"node_id": entry["id"], "node_type": entry.get("type", "concept")}, "edges": []})
