from __future__ import annotations

import re
from typing import Any

import yaml

from sldb.core.renderer_engine.base import BaseRenderer
from sldb.core.handlers.utils import parse_marker


_FRONTMATTER_OPTREV_KEY = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*:\s*⸢([^⸥]+)⸥\s*$")


class YamlRenderer(BaseRenderer):
    """
    Handles rendering of YAML, front-matter, and fence blocks.
    """

    def render(self, node, block_text: str, data: dict[str, Any]) -> str:
        is_front_matter = node.type == "front_matter"
        if is_front_matter:
            front_matter_body = re.sub(r"^---\n?", "", block_text.strip())
            front_matter_body = re.sub(r"\n?---$", "", front_matter_body)
            content = self._render_frontmatter_body(front_matter_body, data)
            return f"---\n{content}\n---"
        content = self.replace_markers(block_text, data)
        return content

    def _render_frontmatter_body(self, body: str, data: dict[str, Any]) -> str:
        lines = []
        for line in body.splitlines():
            rendered = self._render_frontmatter_line(line, data)
            if rendered is not None:
                lines.append(rendered)
        return "\n".join(lines)

    def _render_frontmatter_line(self, line: str, data: dict[str, Any]) -> str | None:
        """One front-matter line. An unused optrev field omits the whole line,
        so the front matter reads exactly as if the field were never declared:
        a None mapping/list VALUE means absent, while `{}`/`[]` are present and
        still dump below. kind == 'render' markers are display-only, so their
        None keeps the historical `null` dump."""
        match = _FRONTMATTER_OPTREV_KEY.match(line)
        if match is None:
            return self.replace_markers(line, data)
        key, marker = match.group(1), parse_marker(match.group(2))
        value = data.get(marker.name)
        if value is None and marker.is_optional:
            return None
        if value is None and not (marker.is_optional or marker.kind == "render"):
            return self.replace_markers(line, data)
        return yaml.safe_dump({key: value}, allow_unicode=True, sort_keys=False).strip()
