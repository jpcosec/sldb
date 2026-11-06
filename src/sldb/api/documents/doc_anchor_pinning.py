"""Pinning on save (GO07, docs/architecture/anchoring.md §6): a `doc:Model:name` without
`@sha256` in a `__doc_anchors__` field or in the provenance `from:` gets the target's contract
hash now. A target the store does not track leaves the value as it is (the anchor reads `lost`
until a later write finds the target); a value already pinned is never re-pinned.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import model_type_of
from sldb.models.doc_anchor_value import PREFIX, anchor_items, pinned
from sldb.models.provenance_block import attach_block, read_block
from sldb.store.edge_index.doc_anchor_states import Current, store_current
from sldb.store.model_contract import doc_anchor, doc_anchor_fields


def pin_payload(store_path: Path, model_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """`payload` with the unpinned anchors of its `__doc_anchors__` fields pinned."""
    names = [n for n in doc_anchor_fields(model_type) if anchor_items(payload.get(n))]
    if not names:
        return payload
    current = store_current(store_path, model_type_of)
    return {**payload, **{n: _pinned_value(payload[n], current) for n in names}}


def pin_provenance(store_path: Path, text: str) -> str:
    """`text` with the unpinned `doc:` items of its provenance `from:` pinned."""
    block = read_block(text) or {}
    items = block.get("from")
    if not isinstance(items, list) or not any(isinstance(i, str) and i.strip().startswith(PREFIX) for i in items):
        return text
    pinned_items = _pinned_value(items, store_current(store_path, model_type_of))
    return text if pinned_items == items else attach_block(text, {**block, "from": pinned_items})


def _pinned_value(value: Any, current: Current) -> Any:
    return [_pin(v, current) for v in value] if isinstance(value, list) else _pin(value, current)


def _pin(value: Any, current: Current) -> Any:
    if (parsed := doc_anchor(value)) is None:
        return value
    exists, now = current(parsed[0])
    return pinned(value, now if exists else None)
