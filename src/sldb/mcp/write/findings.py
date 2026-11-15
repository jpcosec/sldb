"""What SLDB reports about what was just written: on_write alerts and edge-index violations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import document_address
from sldb.mcp.changes import BatchChange


def on_write_alerts(store_path: Path, written: list[BatchChange]) -> list[dict[str, Any]]:
    """The alerts of the `on_write` RuleDocs on what was written (an error would have refused
    the batch), each naming its rule (`rules/<RuleDoc name>`). Only documents that are nodes
    of the edge index can be a rule subject for `rules_check` (see PENDING["on_write_alerts"])."""
    on_write = {f"rules/{r['name']}" for r in api.select_documents(store_path, {"model": "RuleDoc", "where": 'moment = "on_write"', "include_linked": True})}
    subjects = [f"{c.model}/{c.id}" for c in written if api.edge_node(store_path, document_address(f"{c.model}:{c.id}")) is not None]
    if not on_write:
        return []
    found = (f.as_dict() for subject in subjects for f in api.rules_check(store_path, subject))
    return [f for f in found if f["code"] in on_write and f["level"] == "alert"]


def edge_marks(change: BatchChange) -> list[tuple[str, ...]]:
    """How SLDB's edge check names this edge: by its RelationDoc, as `source -[type]-> target`,
    or, for cardinality, as its source with that type's targets or its target with its sources."""
    payload = change.payload or {}
    source, target = document_address(payload.get("source_id", "")), document_address(payload.get("target_id", ""))
    relation = payload.get("relation_type", "")
    return [(f"relation '{change.id}'",), (f"{source} -[{relation}]-> {target}",), (f"{source} has ", f"'{relation}' targets"), (f"{target} has ", f"'{relation}' sources")]


def edge_findings(store_path: Path, edges: list[BatchChange]) -> list[str]:
    """The edge index's violations about the edges just written (SLDB checks edges only
    after the write: see PENDING["edge_validation_before_write"])."""
    if not edges:
        return []
    errors = api.check_edges(store_path, include_linked=False).errors
    marks = [m for c in edges for m in edge_marks(c)]
    return [e for e in errors if any(all(part in e for part in mark) for mark in marks)]
