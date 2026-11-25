"""The edge violations a batch would introduce, found before anything is written.

The batch is applied in memory to the composed edge index (relation types, relations and new
documents of the batch, in request order, so a relation may lean on another of the same batch)
and the index is validated with the very functions `check_edges` uses
(`validate_edge_index_by_store`). Only the violations the batch adds are reported: the ones
the store already had are `check_edges`'s business."""

from __future__ import annotations

import re
from typing import Any

from sldb.api.documents.document_lookup import find_doc
from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBError
from sldb.store.io import load_store_index
from sldb.store.edge_index.doc_kinds import relation_edge, relation_type_contribution
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.node_ids import RELATION_MODEL, RELATION_TYPE_MODEL, doc_node_id, relation_type_node_id
from sldb.store.edge_index.resolve import resolve_authored
from sldb.store.edge_index.validation import validate_edge_index_by_store
from sldb.store.models import EdgeNodeRecord, EdgeRecord

_EDGE = re.compile(r"^edge (?P<source>\S+) -\[(?P<type>.+?)\]-> (?P<target>\S+): (?P<what>.*)$", re.S)
_RELATION = re.compile(r"^relation '(?P<doc>.*?)': (?P<end>source|target) '(?P<id>.*)' is not a tracked document$", re.S)
_CARDINALITY = re.compile(r"^(?P<node>\S+) has \d+ '(?P<type>.+?)' (?P<side>targets|sources) but cardinality is ")
_DOCUMENT = "sldb://document/"
_EDGE_MODELS = (RELATION_MODEL, RELATION_TYPE_MODEL)


def batch_edge_violations(location: StoreLocation, changes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One entry per violation the batch adds: `code` (`types`, `cardinality`, `condition` or
    `endpoint`), `level`, `message` and `relation` (`source`, `type`, `target` as export ids),
    with `relation_doc` the RelationDoc of the batch behind it (None if the batch has none)."""
    changes = [{**c, "model": _model_of(location, c)} for c in changes]
    if not any(c["model"] in _EDGE_MODELS for c in changes):
        return []  # a plain document's creation cannot violate an edge: the index is not even read
    base = load_edge_index(location.store_path, True)
    index, authored, problems = _simulated(base, changes)
    if index is base:
        return []
    known = set(_errors(base))
    found = [m for m in _errors(index) if m not in known] + [p for p in problems if p not in known]
    return [v for message in found for v in _violations(message, authored)]


def _model_of(location: StoreLocation, change: dict[str, Any]) -> str | None:
    """The model a change is over: its own, or the tracked document's (an update or delete names none)."""
    if change.get("model") is not None or change["action"] in ("create", "track"):
        return change.get("model")
    try:
        return find_doc(location.store_path, location.project_root, load_store_index(location.store_path), change["id"])[0].name
    except SLDBError:
        return None


def _errors(index: EdgeIndex) -> list[str]:
    own, linked = validate_edge_index_by_store(index)
    return own + linked


def _simulated(base: EdgeIndex, changes: list[dict[str, Any]]) -> tuple[EdgeIndex, dict[str, dict[str, Any]], list[str]]:
    """The index after the batch, the batch's live relations (doc name -> payload) and the
    problems composing them found."""
    nodes, relations, edges, added = dict(base.nodes), {}, list(base.edges), []
    replaced: set[str] = set()
    for change in changes:
        name, model, action = change["id"], change.get("model"), change["action"]
        if model == RELATION_MODEL and action in ("create", "update", "delete"):
            replaced.add(name)
            relations.pop(name, None)
            if action != "delete" and isinstance(change.get("payload"), dict):
                relations[name] = change["payload"]
        elif model == RELATION_TYPE_MODEL:
            added += _relation_type(nodes, edges, change)
        elif action == "create" and isinstance(model, str):
            nodes.setdefault(doc_node_id(f"{model}:{name}"), EdgeNodeRecord(id=doc_node_id(f"{model}:{name}"), node_type=model, semantics={"name": name, "model": model}))
    if not replaced and not relations and nodes == base.nodes and not added:
        return base, {}, []
    edges = [e for e in edges if e.metadata.get("relation_doc") not in replaced or e.metadata.get("origin") != "relation_doc"] + added
    problems: list[str] = []
    for name, payload in relations.items():
        composed, bad = resolve_authored(relation_edge(name, payload), nodes)
        edges += composed
        problems += bad
    return EdgeIndex(nodes=nodes, edges=edges), relations, problems


def _relation_type(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], change: dict[str, Any]) -> list[EdgeRecord]:
    """A RelationTypeDoc of the batch: its node (and schema edges) replace the document's old
    ones; `edges` without the old, the new edges returned."""
    name = change["id"]
    gone = {k for k, n in nodes.items() if n.node_type == "relation_type" and n.semantics.get("doc") == name}
    for key in gone:
        del nodes[key]
    edges[:] = [e for e in edges if e.source not in gone]
    payload = change.get("payload")
    if change["action"] == "delete" or not isinstance(payload, dict) or not payload.get("name"):
        return []
    part = relation_type_contribution(name, payload)
    nodes.update({n.id: n for n in part.nodes})
    return part.edges


def _export(node_id: str) -> str:
    return node_id[len(_DOCUMENT):] if node_id.startswith(_DOCUMENT) else node_id


def _violations(message: str, authored: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """The entries one violation sentence stands for: one per relation of the batch it names."""
    if (m := _RELATION.match(message)) is not None:
        payload = authored.get(m["doc"], {})
        return [_entry("endpoint", message, m["doc"], payload.get("source_id", ""), payload.get("relation_type", ""), payload.get("target_id", ""))]
    if (m := _EDGE.match(message)) is not None:
        code = "condition" if m["what"].startswith("condition does not parse") else "types"
        return [_entry(code, message, _doc_of(authored, _export(m["source"]), m["type"], _export(m["target"])), _export(m["source"]), m["type"], _export(m["target"]))]
    if (m := _CARDINALITY.match(message)) is not None:
        node, side = _export(m["node"]), m["side"]
        behind = [(n, p) for n, p in authored.items() if p.get("relation_type") == m["type"] and p.get("source_id" if side == "targets" else "target_id") == node]
        return [_entry("cardinality", message, n, p["source_id"], m["type"], p["target_id"]) for n, p in behind] or [_entry("cardinality", message, None, node if side == "targets" else "", m["type"], "" if side == "targets" else node)]
    return [_entry("types", message, None, "", "", "")]


def _doc_of(authored: dict[str, dict[str, Any]], source: str, relation: str, target: str) -> str | None:
    return next((n for n, p in authored.items() if (p.get("source_id"), p.get("relation_type"), p.get("target_id")) == (source, relation, target)), None)


def _entry(code: str, message: str, doc: str | None, source: str, relation: str, target: str) -> dict[str, Any]:
    return {"code": code, "level": "error", "message": message, "relation_doc": doc, "relation": {"source": source, "type": relation, "target": target}}
