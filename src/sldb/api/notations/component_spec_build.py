"""Steps 2-6 of `component_spec_from_graph`: live edges, isolation drop, spec nodes and edges."""

from __future__ import annotations

from typing import NamedTuple

from sldb.api.notations.component_spec_constants import CONTAINS_RELATION, GraphAttrs, GraphEdges
from sldb.api.notations.component_spec_fields import add_groups, apply_fields, field_value
from sldb.api.notations.component_spec_ids import _label_and_kind, _unique_ids


def _live_edges(edges: GraphEdges, kept: dict, include: tuple, exclude: tuple) -> GraphEdges:
    """2. Aristas con ambos extremos vivos y relacion admitida, sin repetir."""
    live: GraphEdges = []
    seen: set[tuple[str, str, str]] = set()
    for source_id, target_id, relation in edges:
        key = (source_id, target_id, relation)
        ok = (relation in include) if include else (relation not in exclude)
        if source_id in kept and target_id in kept and ok and key not in seen:
            seen.add(key)
            live.append(key)
    return live


def _connected(kept: dict, live_edges: GraphEdges) -> dict:
    """3. Sin los nodos aislados."""
    connected = {e[0] for e in live_edges} | {e[1] for e in live_edges}
    return {nid: t for nid, t in kept.items() if nid in connected}


class _Fields(NamedTuple):
    payloads: dict
    label: str | None
    kind: str | None
    group: str | None


def _spec_data(kept: dict, live_edges: GraphEdges, attrs: GraphAttrs, fields: _Fields) -> dict:
    """4. Ids seguros y nodos del spec; 5. `contains` anida, el resto son aristas; 6. grupos."""
    ids = _unique_ids(kept)
    spec_nodes = {ids[nid]: apply_fields(_spec_node(nid, t, attrs.get(nid)), fields.payloads.get(nid), fields.label, fields.kind) for nid, t in kept.items()}
    spec_edges: list[dict] = []
    for source_id, target_id, relation in live_edges:
        if relation != CONTAINS_RELATION:
            spec_edges.append({"from": ids[source_id], "to": ids[target_id], "relation": relation})
        elif ids[target_id] not in spec_nodes[ids[source_id]].setdefault("contains", []):
            spec_nodes[ids[source_id]]["contains"].append(ids[target_id])
    add_groups(spec_nodes, {ids[nid]: field_value(fields.payloads.get(nid), fields.group) for nid in kept})
    return {"nodes": spec_nodes, "edges": spec_edges}


def _spec_node(node_id: str, node_type: str, declared: dict | None) -> dict:
    label, kind = _label_and_kind(node_id, node_type)
    if declared:
        label, kind = declared.get("label") or label, declared.get("kind") or kind
    return {"label": label, "kind": kind}
