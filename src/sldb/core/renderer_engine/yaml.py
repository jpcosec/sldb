from __future__ import annotations

import re
from typing import Any

from sldb.core.renderer_engine.base import BaseRenderer


class YamlRenderer(BaseRenderer):
    """
    Handles rendering of YAML, front-matter, and fence blocks.
    """

    def render(self, node, block_text: str, data: dict[str, Any]) -> str:
        is_front_matter = node.type == "front_matter"
        if is_front_matter:
            front_matter_body = re.sub(r"^---\n?", "", block_text.strip())
            front_matter_body = re.sub(r"\n?---$", "", front_matter_body)
            content = self.replace_markers(front_matter_body, data)
            return f"---\n{content}\n---"
        content = self.replace_markers(block_text, data)
        return content
