"""The planning step of `rewrite_references` (GD22): the new payload of each referring document and
the new text of each mentioning file, validated in memory under its model before anything is
written (docs/architecture/references.md).
"""

from __future__ import annotations

from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.referrers import Hit, Target, matching_documents
from sldb.api.edges.rewrite_mentions import rewritten_text
from sldb.api.edges.rewrite_values import rewritten_payload
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import validate_model_data_roundtrip, validate_model_input_roundtrip
from sldb.store.source_guard import aggregate_text

Plan = tuple[str, dict[str, Any], list[dict[str, Any]]]
TextPlan = tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]


def planned_payload(location: StoreLocation, pythonpath: str | None, export_id: str, hits: list[Hit], target: Target, replacement: Target | None) -> Plan:
    """(path, new payload, changes) of one referring document, its payload validated under its model."""
    doc = runtime_document(location.store_path, pythonpath, export_id.replace(":", "/", 1))
    payload, changes = rewritten_payload(dict(doc.payload), [(r, v) for r, v in hits if v is not None], target, replacement)
    _check(export_id, _model_type(location, pythonpath, doc.model_name), payload, None)
    return doc.path, payload, changes


def planned_text(location: StoreLocation, graph: ProjectGraph | None, pythonpath: str | None, path: str, hits: list[Hit], target: Target, replacement: Target | None) -> TextPlan:
    """(path, text, new text, changes, skips) of one mentioning file, a tracked document's new text validated."""
    if (text := aggregate_text(location.project_root, location.project_root / path, path)) is None:
        return path, "", "", [], [{"source": path, "location": None, "reason": "not read: the path resolves outside the project root or is a symlink"}]
    new_text, changes, skips = rewritten_text(text, graph, path, hits, target, replacement)
    for document in matching_documents(location.store_path, path) if new_text != text else []:
        _check(f"{document['model']}:{document['name']}", _model_type(location, pythonpath, document["model"]), None, new_text)
    return path, text, new_text, changes, skips


def _model_type(location: StoreLocation, pythonpath: str | None, model: str) -> type:
    return load_registered_model(location.store_path, model, pythonpath).model_type


def _check(node: str, model_type: type, payload: dict[str, Any] | None, text: str | None) -> None:
    """The new payload (or text) must validate and round-trip under the model, else `SLDBValidationError` and nothing is written."""
    try:
        valid, details = validate_model_data_roundtrip(model_type, payload) if payload is not None else validate_model_input_roundtrip(model_type, text or "")
    except (ValueError, TypeError) as exc:
        raise SLDBValidationError(f"{node}: the rewritten document does not validate under {model_type.__name__}: {exc}") from exc
    if not valid:
        raise SLDBValidationError(f"{node}: the rewritten document does not round-trip under {model_type.__name__}; nothing written", details)
