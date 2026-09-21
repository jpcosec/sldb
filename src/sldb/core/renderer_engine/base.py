from __future__ import annotations

import re
from typing import Any

import yaml
from jinja2 import Environment

from sldb.core.handlers.utils import parse_marker
from sldb.core.renderer_engine.python_expr import PythonExpressionRenderer


class BaseRenderer:
    """
    Base class for rendering components.
    """

    def __init__(self, jinja_env: Environment):
        self.jinja_env = jinja_env
        self.py_renderer = PythonExpressionRenderer()

    def replace_markers(self, text: str, data: dict[str, Any]) -> str:
        lines = []
        for line in text.split("\n"):
            if self._is_absent_optional_line(line, data):
                continue
            lines.append(re.sub(r"⸢([^⸥]+)⸥", lambda m: self._sub_marker(m, data), line))
        return self.jinja_env.from_string("\n".join(lines)).render(**data)

    def _is_absent_optional_line(self, line: str, data: dict[str, Any]) -> bool:
        """An optrev marker whose value is None leaves NO trace in the render:
        its whole line is dropped, so the document reads byte-for-byte as if
        the field were never declared (contract: 'It MAY BE ABSENT in the
        document'). Only two shapes qualify: `key: ⸢optrev•key⸥` or
        `⸢optrev•key⸥` alone on the line (leading whitespace allowed).

        A line that SHARES its content with anything else -- a table row of
        cells, a list bullet, preceding text, another marker -- is never
        dropped; there the marker is replaced with the empty string (today's
        behavior) because deleting the line would corrupt the surrounding
        structure (a table would lose a column, a list item would vanish).
        An empty list/dict VALUE (`[]`/`{}`) is not None, so it still renders
        (as an empty table or empty mapping); only a None value means absent.

        kind == 'render' markers are NOT optional-extractable fields: they
        keep their historical empty-string behavior and are never the reason
        a line is omitted.
        """
        m = re.match(r"^\s*(?:[A-Za-z0-9_-]+\s*:\s*)?⸢([^⸥]+)⸥\s*$", line)
        if not m:
            return False
        marker = parse_marker(m.group(1))
        if not marker.is_optional:
            return False
        return data.get(marker.name) is None

    def _sub_marker(self, match: re.Match, data: dict[str, Any]) -> str:
        m = parse_marker(match.group(1))
        if m.kind == "py": return self.py_renderer.render(m.name, data, match.group(0))
        val = data.get(m.name)
        if val is None: return "" if m.is_optional or m.kind == "render" else match.group(0)
        if self._is_table_marker(m): return self._render_markdown_table(val, self._table_columns(m, val))
        return self._format_value(val, m)

    def _format_value(self, val: Any, marker: Any) -> str:
        if "dict" in marker.traits or isinstance(val, (dict, list)):
            if "list" in marker.traits and not isinstance(val, (dict, list)): return str(val)
            return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()
        return str(val)

    def _is_table_marker(self, marker: Any) -> bool:
        return any(trait == "table" or trait.startswith("table[") for trait in marker.traits)

    def _table_columns(self, marker: Any, value: Any) -> list[str]:
        for trait in marker.traits:
            if trait.startswith("table[") and trait.endswith("]"):
                return [col.strip() for col in trait[6:-1].split(",") if col.strip()]
        if isinstance(value, list) and value:
            first = value[0].model_dump() if hasattr(value[0], "model_dump") else value[0]
            if isinstance(first, dict): return [str(key) for key in first.keys()]
        return []

    def _render_markdown_table(self, value: Any, columns: list[str]) -> str:
        if not columns: return "| |\n| --- |"
        res = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
        for row in (value if isinstance(value, list) else []):
            rd = row.model_dump() if hasattr(row, "model_dump") else row
            res.append("| " + " | ".join([self._format_table_cell((rd if isinstance(rd, dict) else {}).get(c, "")) for c in columns]) + " |")
        return "\n".join(res)

    def _format_table_cell(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).replace("\n", " ").replace("|", "\\|")

    def get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        """Helper to get node source from block text."""
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])
