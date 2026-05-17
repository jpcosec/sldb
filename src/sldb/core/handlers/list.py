from __future__ import annotations

import re
from typing import Any

from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"


class ListNodeHandler(BaseNodeHandler):
    """
    Handler for extracting data from list nodes.
    """

    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        items = [child for child in node.children if child.type == "list_item"]
        if not items:
            return []

        recipes = []
        for item in items:
            text = self.get_text(item).strip()
            match = re.search(MARKER_PATTERN, text)
            if match:
                marker = parse_marker(match.group(1))
                if marker.is_reversible or marker.is_optional:
                    recipes.append(
                        {
                            "name": marker.name,
                            "marker": marker,
                            "handler": "list",
                            "item_template": text,
                        }
                    )
        return recipes

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        items = [child for child in node.children if child.type == "list_item"]
        values = []
        for item in items:
            self.router.get_handler_for_node(item)
            text = self.router.handlers["text"].get_text(item).strip()
            if text == "":
                continue
            values.append(text)
        return {recipe["name"]: values}
