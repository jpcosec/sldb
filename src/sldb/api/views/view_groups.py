"""Rows grouped by one field, in a declared order (GD25, q10)."""

from __future__ import annotations

from typing import Any


def grouped(rows: list[dict[str, Any]], group_by: str, group_order: list[str]) -> list[dict[str, Any]]:
    """`[{value, rows}]`: first `group_order`'s values (each present, rows or not), then the
    other values sorted, then the rows without the field under `value: null`."""
    by_value: dict[Any, list[dict[str, Any]]] = {}
    for row in rows:
        by_value.setdefault(_value(row, group_by), []).append(row)
    declared = [{"value": value, "rows": by_value.pop(value, [])} for value in group_order]
    missing = by_value.pop(None, [])
    others = [{"value": value, "rows": by_value[value]} for value in sorted(by_value, key=str)]
    return declared + others + ([{"value": None, "rows": missing}] if missing else [])


def _value(row: dict[str, Any], group_by: str) -> Any:
    """The scalar the row shows for the field; a list or mapping groups as its text form."""
    value = row["fields"].get(group_by)
    if value is None:
        return None
    return value if isinstance(value, (str, int, float, bool)) else str(value)
