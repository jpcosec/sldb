"""Serialization of search records: the shape `sldb find --format json` emits.

Lives here, not in the CLI formatter, because `sldb.api.search` returns this payload to
library consumers; the CLI formatter only chooses text/yaml/json framing around it.
"""

from __future__ import annotations

from typing import Any

from sldb.api.records.search_record import SearchRecord


def serialize_record(record: SearchRecord) -> dict[str, Any]:
    """One record as its JSON mapping; doc records also carry their semantic tags."""
    data = record.as_dict()
    if record.kind == "doc":
        data["semantic_tags"] = list(record.semantic)
        data["provenance"] = record.provenance
    return data


def serialize_records(records: list[SearchRecord]) -> list[dict[str, Any]]:
    """Every record as its JSON mapping, order preserved."""
    return [serialize_record(record) for record in records]


def select_keys(payload: list[dict[str, Any]], select: str) -> list[dict[str, Any]]:
    """Narrow each mapping to the comma-separated keys in `select`, missing keys as None."""
    fields = [part.strip() for part in select.split(",") if part.strip()]
    return [{key: item.get(key) for key in fields} for item in payload]
