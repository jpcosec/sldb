from typing import Any
from sldb.core.node import SLDBNode
from sldb.core.node_handler import SharedNodeHandler

class RecipeMatcher:
    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def _find_leaf_text_node(self, node: SLDBNode) -> SLDBNode | None:
        if node.type == "text" or node.content: return node
        for child in node.children:
            if result := self._find_leaf_text_node(child): return result
        return None

    def match_recipe_at_block(self, block: SLDBNode, recipe: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
        if not self.check_type_and_tag(block, recipe): return False, None
        return self._evaluate_handler(block, recipe)

    def check_type_and_tag(self, block: SLDBNode, recipe: dict[str, Any]) -> bool:
        if block.type != recipe["outer_type"]: return False
        is_anchor, outer_tag = recipe.get("anchor", False), recipe.get("outer_tag", "")
        if not is_anchor and block.tag != outer_tag: return False
        return not (is_anchor and outer_tag and block.tag != outer_tag)

    def _evaluate_handler(self, block: SLDBNode, recipe: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
        handler_key = recipe.get("handler", "text")
        current_node = self._find_leaf_text_node(block) if handler_key == "text" else block
        is_anchor = recipe.get("anchor", False)
        if not current_node: return (True, {}) if is_anchor else (False, None)
        values = self.node_handler.handlers[handler_key].extract_data(current_node, recipe)
        return (True, values) if is_anchor or values else (False, None)

    def block_matches_recipe_for_position(self, block: SLDBNode, recipe: dict[str, Any]) -> bool:
        if not self.check_type_and_tag(block, recipe): return False
        if recipe.get("handler", "text") == "text":
            content = self.node_handler.handlers["text"].get_text(block)
            return self.node_handler.handlers["text"].matches(content, recipe)
        return self.match_recipe_at_block(block, recipe)[0]
