from __future__ import annotations

import re
from typing import Any

from sldb.core.handlers.list_escape import escape_item
from sldb.core.renderer_engine.base import BaseRenderer


class ListRenderer(BaseRenderer):
    """
    Handles rendering of list blocks.
    """

    def render(self, node, block_text: str, data: dict[str, Any], block_start_line: int) -> str:
        if not node.children: return self.replace_markers(block_text, data)
        item_text = self.get_node_source(node.children[0], block_text, block_start_line)
        match = re.search(r"⸢([^⸥]+)⸥", item_text)
        if not match: return self.replace_markers(block_text, data)
        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
        return self._render_items(item_text, data.get(root_prop, []), root_prop)

    def _render_items(self, item_text: str, list_items: Any, root_prop: str) -> str:
        if not isinstance(list_items, list): return ""
        if not list_items: return self.replace_markers(item_text, {root_prop: ""})
        rendered_items, bare = [], _value_opens_item(item_text)
        for index, item in enumerate(list_items):
            d = item if isinstance(item, dict) else {root_prop: escape_item(item) if bare and isinstance(item, str) else item}
            rendered_items.append(self._render_item(item_text, d, f"{root_prop}/{index}", None if isinstance(item, dict) else root_prop))
        return "\n".join(rendered_items)

    def _render_item(self, item_text: str, data: dict[str, Any], prefix: str, scalar_root: str | None) -> str:
        """One list item, with every recorded path scoped under its index.

        Args:
            item_text: The template of a single item.
            data: The item's payload mapping.
            prefix: Path of the item, such as ``steps/2``.
            scalar_root: Root property name when the item is a scalar, else None.

        Returns:
            The rendered item.
        """
        if self.recorder is None:
            return self.replace_markers(item_text, data)
        with self.recorder.item_scope(prefix, scalar_root):
            return self.replace_markers(item_text, data)


def _value_opens_item(item_text: str) -> bool:
    """`- ⸢rev,list•x⸥`: the value is the item's whole text, so block syntax in it would be read."""
    return re.sub(r"^\s*([-+*]|\d+[.)])\s+", "", item_text).startswith("⸢")
