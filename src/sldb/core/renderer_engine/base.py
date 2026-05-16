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
        """
        Replaces ⸢...⸥ markers in the provided text.
        """

        def sub_marker(match):
            marker = parse_marker(match.group(1))

            if marker.kind == "py":
                return self.py_renderer.render(marker.name, data, match.group(0))

            val = data.get(marker.name)
            if val is None:
                if marker.is_optional or marker.kind == "render":
                    return ""
                return match.group(0)

            if "dict" in marker.traits or isinstance(val, (dict, list)):
                if "list" in marker.traits and not isinstance(val, (dict, list)):
                    return str(val)
                return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()

            return str(val)

        rendered = re.sub(r"⸢([^⸥]+)⸥", sub_marker, text)
        return self.jinja_env.from_string(rendered).render(**data)

    def get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        """Helper to get node source from block text."""
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])
