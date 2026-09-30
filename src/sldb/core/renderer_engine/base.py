from __future__ import annotations

import re
from typing import Any

import yaml
from jinja2 import Environment

from sldb.core.handlers.utils import parse_marker
from sldb.core.renderer_engine.jinja_trailing import unshield_trailing_newline
from sldb.core.renderer_engine.python_expr import PythonExpressionRenderer
from sldb.core.renderer_engine.table_markdown import format_table_cell, is_table_marker, render_markdown_table, table_columns


class BaseRenderer:
    """
    Base class for rendering components.
    """

    def __init__(self, jinja_env: Environment, recorder: Any = None):
        self.jinja_env = jinja_env
        self.py_renderer = PythonExpressionRenderer()
        self.recorder = recorder

    def replace_markers(self, text: str, data: dict[str, Any]) -> str:
        lines = []
        for line in text.split("\n"):
            if self._is_absent_optional_line(line, data):
                continue
            lines.append(re.sub(r"⸢([^⸥]+)⸥", lambda m: self._sub_marker(m, data), line))
        source = "\n".join(lines)
        if self.recorder is not None:
            source = unshield_trailing_newline(source)
        return self.jinja_env.from_string(source).render(**data)

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
        out = self._resolve_marker(m, match, data)
        if self.recorder is None or out == match.group(0):
            return out
        return self.recorder.wrap(out, self.recorder.meta_for(m))

    def _resolve_marker(self, m: Any, match: re.Match, data: dict[str, Any]) -> str:
        """The rendered surface of one marker, or the literal marker when unresolved.

        Args:
            m: The parsed marker.
            match: The regex match of the marker in the template line.
            data: The payload the marker reads from.

        Returns:
            The value's text, an empty string for an absent optional, or the
            literal marker when the value is missing and required.
        """
        if m.kind == "py": return self.py_renderer.render(m.name, data, match.group(0))
        val = data.get(m.name)
        if val is None: return "" if m.is_optional or m.kind == "render" else match.group(0)
        if is_table_marker(m): return render_markdown_table(val, table_columns(m, val))
        return self._format_value(val, m)

    def _format_value(self, val: Any, marker: Any) -> str:
        if "dict" in marker.traits or isinstance(val, (dict, list)):
            if "list" in marker.traits and not isinstance(val, (dict, list)): return str(val)
            return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()
        return str(val)

    _is_table_marker = staticmethod(is_table_marker)
    _table_columns = staticmethod(table_columns)
    _render_markdown_table = staticmethod(render_markdown_table)
    _format_table_cell = staticmethod(format_table_cell)

    def get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        """Helper to get node source from block text."""
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])
