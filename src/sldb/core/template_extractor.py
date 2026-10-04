import re
from typing import Any
from sldb.core.exceptions import SLDBASTError
from sldb.core.node import SLDBNode
from sldb.core.node_handler import SharedNodeHandler

class TemplateExtractor:
    """Extracts deterministic search recipes from template block nodes."""

    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def extract_nodes(self, block_nodes: list[SLDBNode]) -> list[dict[str, Any]]:
        extracted_recipes = []
        for outer_index, block_node in enumerate(block_nodes):
            state = {"found": False, "recipes": extracted_recipes, "idx": outer_index, "node": block_node}
            self._dive(block_node, [], state)
            if not state["found"]: self._add_anchor_recipe(state)
        self._validate_invariants(extracted_recipes)
        return extracted_recipes

    def _dive(self, node: SLDBNode, current_path: list[int], state: dict[str, Any]) -> None:
        handler_key = self.node_handler.get_handler_for_node(node)
        if handler_key and handler_key != "text" and self._process_non_text_handler(node, current_path, state, handler_key): return
        if (handler_key == "text" or not node.children) and self._process_text_handler(node, current_path, state): return
        for child_idx, child in enumerate(node.children):
            self._dive(child, current_path + [child_idx], state)

    def _process_non_text_handler(self, node: SLDBNode, current_path: list[int], state: dict[str, Any], handler_key: str) -> bool:
        handler_recipes = self.node_handler.handlers[handler_key].compile_recipe(node)
        if not handler_recipes: return False
        for recipe in handler_recipes:
            self._update_and_append_recipe(recipe, state, current_path)
            state["found"] = True
        return True

    def _process_text_handler(self, node: SLDBNode, current_path: list[int], state: dict[str, Any]) -> bool:
        literal_recipes = self.node_handler.handlers["text"].compile_recipe(node)
        if not literal_recipes: return False
        for recipe in literal_recipes:
            self._check_section_body(recipe, node, state)
            self._update_and_append_recipe(recipe, state, current_path)
            state["found"] = True
        return True

    def _check_section_body(self, recipe: dict[str, Any], node: SLDBNode, state: dict[str, Any]) -> None:
        """Mark a lone marker in its own paragraph as owning the section body.

        `rev` and `optrev` both qualify. The condition used to read `is_reversible`
        alone, and that made `optrev` fall through to the regex path, where
        `re.fullmatch(r"^(.*?)$", ...)` runs without `re.S`: a soft line break did
        not match and the field came back empty. The two markers differ in whether
        the field may be absent, never in how its text is captured.
        """
        block_text = self.node_handler.handlers["text"].get_text(node).strip()
        outer_type = state["node"].type
        if (outer_type == "paragraph" and len(recipe.get("props_info", [])) == 1
            and block_text.startswith("⸢") and block_text.endswith("⸥")
            and recipe.get("regex") == "^(.*?)$" and (recipe["props_info"][0].is_reversible or recipe["props_info"][0].is_optional)):
            recipe["capture_mode"] = "section_body"

    def _update_and_append_recipe(self, recipe: dict[str, Any], state: dict[str, Any], current_path: list[int]) -> None:
        recipe.update({
            "outer_index": state["idx"],
            "outer_type": recipe.get("match_outer_type", state["node"].type),
            "outer_tag": recipe.get("match_outer_tag", state["node"].tag),
            "inner_path": current_path,
        })
        state["recipes"].append(recipe)

    def _add_anchor_recipe(self, state: dict[str, Any]) -> None:
        content = self.node_handler.handlers["text"].get_text(state["node"]).strip()
        state["recipes"].append({
            "outer_index": state["idx"], "outer_type": state["node"].type, "outer_tag": state["node"].tag,
            "inner_path": [], "props": [], "regex": f"^{re.escape(content)}$" if content else "^$",
            "handler": "text", "anchor": True,
        })

    def _validate_invariants(self, recipes: list[dict[str, Any]]) -> None:
        rev_counts = {}
        for recipe in recipes:
            for marker in self._extract_markers(recipe):
                if marker.is_reversible: rev_counts[marker.name] = rev_counts.get(marker.name, 0) + 1
        for name, count in rev_counts.items():
            if count > 1: raise SLDBASTError(f"Multiple canonical 'rev' markers found for field '{name}'.")

    def _extract_markers(self, recipe: dict[str, Any]) -> list[Any]:
        if "props_info" in recipe: return recipe["props_info"]
        if "marker" in recipe: return [recipe["marker"]]
        if "markers" in recipe: return [item["marker"] for item in recipe["markers"]]
        return []
