"""Turn one recorded span into the segment dict the contract describes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.segments.payload_values import kind_at, value_at
from sldb.api.segments.segment_display import display_of
from sldb.api.segments.segment_enrichment import enrich_segment

EDITABLE_MARKERS = ("rev", "optrev")
EXTRA_KEYS = ("composition", "ref_index", "ref", "projection", "table_data")


def build_node(
    meta: dict[str, Any],
    start: int,
    end: int,
    text: str,
    model_type: type,
    payload: dict[str, Any],
    store_path: Path | None = None,
    pythonpath: str | None = None,
) -> dict[str, Any]:
    """The segment dict for one recorded span."""
    node = _base_node(meta, start, end, text)
    node.update({key: meta[key] for key in EXTRA_KEYS if key in meta})
    if node["type"] == "field" and meta.get("source") is None:
        node["kind"] = kind_at(model_type, meta["path"])
        node["value"] = value_at(payload, meta["path"])
    return enrich_segment(node, store_path, pythonpath)


def _base_node(meta: dict[str, Any], start: int, end: int, text: str) -> dict[str, Any]:
    marker = meta.get("marker", "compose" if meta.get("piece") else "")
    return {
        "type": "composition" if meta.get("piece") else "field",
        "start": start, "end": end, "text": text[start:end],
        "path": meta.get("path", ""), "marker": marker, "traits": list(meta.get("traits") or []),
        "editable": marker in EDITABLE_MARKERS,
        "display": display_of(text, start, end),
        "source": meta.get("source"), "children": [], "_order": meta["_order"],
    }
