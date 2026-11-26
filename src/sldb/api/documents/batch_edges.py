"""The edge violations a batch would introduce, found before anything is written.

The batch is applied in memory to the composed edge index (relation types, relations and new
documents of the batch, in request order, so a relation may lean on another of the same batch)
and the index is validated with the very functions `check_edges` uses
(`validate_edge_index_by_store`). Only the violations the batch adds are reported: the ones
the store already had are `check_edges`'s business."""

from __future__ import annotations

import re
from typing import Any

from sldb.api.documents.batch_simulation import simulated
from sldb.api.documents.document_lookup import find_doc
from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBError
from sldb.store.io import load_store_index
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.node_ids import RELATION_MODEL, RELATION_TYPE_MODEL
from sldb.store.edge_index.validation import validate_edge_index_by_store

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
    index, authored, problems = simulated(base, changes)
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
        return _cardinality(message, m, authored)
    return [_entry("types", message, None, "", "", "")]


def _cardinality(message: str, m: re.Match[str], authored: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    node, side = _export(m["node"]), m["side"]
    behind = [(n, p) for n, p in authored.items() if p.get("relation_type") == m["type"] and p.get("source_id" if side == "targets" else "target_id") == node]
    return [_entry("cardinality", message, n, p["source_id"], m["type"], p["target_id"]) for n, p in behind] or [_entry("cardinality", message, None, node if side == "targets" else "", m["type"], "" if side == "targets" else node)]


def _doc_of(authored: dict[str, dict[str, Any]], source: str, relation: str, target: str) -> str | None:
    return next((n for n, p in authored.items() if (p.get("source_id"), p.get("relation_type"), p.get("target_id")) == (source, relation, target)), None)


def _entry(code: str, message: str, doc: str | None, source: str, relation: str, target: str) -> dict[str, Any]:
    return {"code": code, "level": "error", "message": message, "relation_doc": doc, "relation": {"source": source, "type": relation, "target": target}}
