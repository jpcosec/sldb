from __future__ import annotations

import re
from typing import Any

from sldb.core.renderer_engine.base import BaseRenderer


class TableRenderer(BaseRenderer):
    """
    Handles rendering of table blocks.
    """

    def render(self, node, block_text: str, data: dict[str, Any]) -> str:
        lines = block_text.splitlines()
        if len(lines) < 3:
            return self.replace_markers(block_text, data)

        header = lines[0]
        separator = lines[1]
        row_template = lines[2]

        match = re.search(r"⸢([^⸥]+)⸥", row_template)
        if not match:
            return self.replace_markers(block_text, data)

        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()

        rows_data = data.get(root_prop, {})
        items_to_render = []
        if isinstance(rows_data, dict):
            sorted_keys = sorted(
                rows_data.keys(), key=lambda x: int(x) if str(x).isdigit() else x
            )
            items_to_render = [rows_data[key] for key in sorted_keys]
        elif isinstance(rows_data, list):
            items_to_render = rows_data

        rendered_rows = []
        for item in items_to_render:
            item_data = item.model_dump() if hasattr(item, "model_dump") else item
            rendered_rows.append(self.replace_markers(row_template, item_data))

        if rendered_rows:
            return "\n".join([header, separator] + rendered_rows)

        return self.replace_markers(block_text, data)
