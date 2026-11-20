"""The field values of tracked documents that name a moved path, rewritten in a copy of the payload."""

from __future__ import annotations

import json
from typing import Any

from sldb.api.documents.move_path_remap import Remap


def rewrite_value(value: Any, remap: Remap, path: str, changes: list[dict[str, Any]]) -> Any:
    """`value` with every string equal to the old path (or under it) replaced; `changes` records each."""
    if isinstance(value, str):
        return _string(value, remap, path, changes)
    if isinstance(value, list):
        return [rewrite_value(item, remap, _join(path, i), changes) for i, item in enumerate(value)]
    if isinstance(value, dict):
        return {key: rewrite_value(item, remap, _join(path, key), changes) for key, item in value.items()}
    return value


def planned_fields(documents: list[Any], remap: Remap) -> list[tuple[Any, dict[str, Any], list[dict[str, Any]]]]:
    """`(document, new payload, changes)` for each document holding the old path in a field."""
    plans = []
    for doc in documents:
        changes: list[dict[str, Any]] = []
        payload = rewrite_value(json.loads(json.dumps(doc.payload)), remap, "", changes)
        if changes:
            plans.append((doc, payload, [{"document": f"{doc.model_name}:{doc.name}", **c} for c in changes]))
    return plans


def _string(value: str, remap: Remap, path: str, changes: list[dict[str, Any]]) -> str:
    new = remap.apply(value)
    if new is None:
        return value
    changes.append({"field": path, "old": value, "new": new})
    return new


def _join(path: str, key: Any) -> str:
    return f"{path}.{key}" if path else str(key)
