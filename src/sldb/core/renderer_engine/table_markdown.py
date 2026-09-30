"""Markdown table emission for ``table``/``table[...]`` markers.

Split out of :mod:`sldb.core.renderer_engine.base` so that module stays inside the
repo's file-size budget once the span recorder is wired in. Behaviour is unchanged:
these are the same routines ``BaseRenderer`` used to carry as methods.
"""

from __future__ import annotations

from typing import Any


def is_table_marker(marker: Any) -> bool:
    """Whether a marker asks for a Markdown table.

    Args:
        marker: A parsed marker.

    Returns:
        True when any trait is ``table`` or ``table[...]``.
    """
    return any(trait == "table" or trait.startswith("table[") for trait in marker.traits)


def table_columns(marker: Any, value: Any) -> list[str]:
    """Column names for a table marker, declared or inferred from the first row.

    Args:
        marker: A parsed marker carrying the table trait.
        value: The value to render, normally a list of rows.

    Returns:
        The column names, empty when none can be determined.
    """
    for trait in marker.traits:
        if trait.startswith("table[") and trait.endswith("]"):
            return [col.strip() for col in trait[6:-1].split(",") if col.strip()]
    if isinstance(value, list) and value:
        first = value[0].model_dump() if hasattr(value[0], "model_dump") else value[0]
        if isinstance(first, dict): return [str(key) for key in first.keys()]
    return []


def render_markdown_table(value: Any, columns: list[str]) -> str:
    """A Markdown table for ``value`` over ``columns``.

    Args:
        value: The rows to render; anything not a list renders as headers only.
        columns: The column names, in order.

    Returns:
        The table as Markdown, or a one-empty-column table when no columns.
    """
    if not columns: return "| |\n| --- |"
    res = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in (value if isinstance(value, list) else []):
        rd = row.model_dump() if hasattr(row, "model_dump") else row
        res.append("| " + " | ".join([format_table_cell((rd if isinstance(rd, dict) else {}).get(c, "")) for c in columns]) + " |")
    return "\n".join(res)


def format_table_cell(value: Any) -> str:
    """One cell's text, with newlines flattened and pipes escaped.

    Args:
        value: The cell value; None renders empty.

    Returns:
        The cell's Markdown-safe text.
    """
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("|", "\\|")
