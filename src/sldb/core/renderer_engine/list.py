from __future__ import annotations

import re
from typing import Any

from sldb.core.renderer_engine.base import BaseRenderer


class ListRenderer(BaseRenderer):
    """
    Handles rendering of list blocks.
    """

    def render(self, node, block_text: str, data: dict[str, Any], block_start_line: int) -> str:
        if not node.children:
            return self.replace_markers(block_text, data)

        first_item = node.children[0]
        item_text = self.get_node_source(first_item, block_text, block_start_line)

        match = re.search(r"⸢([^⸥]+)⸥", item_text)
        if not match:
            return self.replace_markers(block_text, data)

        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()

        list_items_data = data.get(root_prop, [])
        if not isinstance(list_items_data, list):
            return ""

        rendered_items = []
        for item_data in list_items_data:
            if isinstance(item_data, dict):
                rendered_items.append(self.replace_markers(item_text, item_data))
            else:
                rendered_items.append(
                    self.replace_markers(item_text, {root_prop: item_data})
                )

        return "\n".join(rendered_items)
