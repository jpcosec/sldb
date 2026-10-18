from __future__ import annotations
import re
from typing import Any
from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.list_escape import unescape_item
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"

class ListNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        items = [child for child in node.children if child.type == "list_item"]
        recipes = []
        for item in items:
            self._process_list_item_for_recipe(item, recipes)
        return recipes

    def _process_list_item_for_recipe(self, item: SLDBNode, recipes: list[dict[str, Any]]) -> None:
        text = self.get_text(item).strip()
        if match := re.search(MARKER_PATTERN, text):
            marker = parse_marker(match.group(1))
            if marker.is_reversible or marker.is_optional:
                recipes.append({"name": marker.name, "marker": marker, "handler": "list", "item_template": text})

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        items = [child for child in node.children if child.type == "list_item"]
        values, bare = [], recipe.get("item_template", "").startswith("⸢")
        for item in items:
            if text := self._extract_text_from_item(item):
                values.append(unescape_item(text) if bare else text)
        return {recipe["name"]: values}

    def _extract_text_from_item(self, item: SLDBNode) -> str:
        self.router.get_handler_for_node(item)
        return self.router.handlers["text"].get_text(item).strip()
