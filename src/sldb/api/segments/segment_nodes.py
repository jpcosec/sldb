"""Turn one recorded span into the segment dict the contract describes.

A span only knows its offsets, its marker and its path. Everything else the UI
needs — the typed value, the field kind, whether the field is editable, whether
it owns a block — is derived here, once, so the tree builder stays about nesting.
A span carrying a ``source`` came from a composed piece: its value lives in
another document, so no kind or value is attached to it.
"""

from __future__ import annotations

from typing import Any

from sldb.api.segments.payload_values import kind_at, value_at
from sldb.api.segments.segment_display import display_of

EDITABLE_MARKERS = ("rev", "optrev")
EXTRA_KEYS = ("composition", "ref_index", "ref")


def build_node(meta: dict[str, Any], start: int, end: int, text: str, model_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """The segment dict for one recorded span.

    Args:
        meta: Recorded span metadata, carrying ``path``, ``marker`` and ``_order``.
        start: Inclusive start offset of the span in ``text``.
        end: Exclusive end offset of the span in ``text``.
        text: The canonical document text.
        model_type: The model the document is rendered through.
        payload: The payload the text was rendered from.

    Returns:
        A ``field`` or ``composition`` segment dict, ready for nesting.
    """
    node = _base_node(meta, start, end, text)
    node.update({key: meta[key] for key in EXTRA_KEYS if key in meta})
    if node["type"] == "field" and meta.get("source") is None:
        node["kind"] = kind_at(model_type, meta["path"])
        node["value"] = value_at(payload, meta["path"])
    return node


def _base_node(meta: dict[str, Any], start: int, end: int, text: str) -> dict[str, Any]:
    """The keys every recorded segment carries, whatever its type.

    Args:
        meta: Recorded span metadata.
        start: Inclusive start offset of the span in ``text``.
        end: Exclusive end offset of the span in ``text``.
        text: The canonical document text.

    Returns:
        A segment dict without value, kind or composition details.
    """
    return {
        "type": "composition" if meta.get("piece") else "field",
        "start": start, "end": end, "text": text[start:end],
        "path": meta["path"], "marker": meta["marker"], "traits": list(meta.get("traits") or []),
        "editable": meta["marker"] in EDITABLE_MARKERS,
        "display": display_of(text, start, end),
        "source": meta.get("source"), "children": [], "_order": meta["_order"],
    }
