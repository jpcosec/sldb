import re
from typing import Any

from sldb.core.exceptions import SLDBASTError
from sldb.core.node import SLDBNode
from sldb.core.node_handler import SharedNodeHandler


class TemplateExtractor:
    """
    Extracts deterministic search recipes from template block nodes.
    """

    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def extract_nodes(self, block_nodes: list[SLDBNode]) -> list[dict[str, Any]]:
        extracted_recipes = []

        for outer_index, block_node in enumerate(block_nodes):
            outer_type = block_node.type
            found_recipe_in_block = False

            def dive(node: SLDBNode, current_path: list[int]):
                nonlocal found_recipe_in_block
                handler_key = self.node_handler.get_handler_for_node(node)

                if handler_key and handler_key != "text":
                    handler_recipes = self.node_handler.handlers[
                        handler_key
                    ].compile_recipe(node)
                    if handler_recipes:
                        for recipe in handler_recipes:
                            recipe.update(
                                {
                                    "outer_index": outer_index,
                                    "outer_type": outer_type,
                                    "outer_tag": block_node.tag,
                                    "inner_path": current_path,
                                }
                            )
                            extracted_recipes.append(recipe)
                            found_recipe_in_block = True
                        return

                if handler_key == "text" or not node.children:
                    literal_recipes = self.node_handler.handlers["text"].compile_recipe(
                        node
                    )
                    if literal_recipes:
                        for recipe in literal_recipes:
                            block_text = (
                                self.node_handler.handlers["text"]
                                .get_text(node)
                                .strip()
                            )
                            if (
                                outer_type == "paragraph"
                                and len(recipe.get("props_info", [])) == 1
                                and block_text.startswith("⸢")
                                and block_text.endswith("⸥")
                                and recipe.get("regex") == "^(.*?)$"
                            ):
                                recipe["capture_mode"] = "section_body"
                            recipe.update(
                                {
                                    "outer_index": outer_index,
                                    "outer_type": outer_type,
                                    "outer_tag": block_node.tag,
                                    "inner_path": current_path,
                                }
                            )
                            extracted_recipes.append(recipe)
                            found_recipe_in_block = True
                        return  # STOP DIVING

                for child_idx, child in enumerate(node.children):
                    dive(child, current_path + [child_idx])

            dive(block_node, [])
            if not found_recipe_in_block:
                content = (
                    self.node_handler.handlers["text"].get_text(block_node).strip()
                )
                extracted_recipes.append(
                    {
                        "outer_index": outer_index,
                        "outer_type": outer_type,
                        "outer_tag": block_node.tag,
                        "inner_path": [],
                        "props": [],
                        "regex": f"^{re.escape(content)}$" if content else "^$",
                        "handler": "text",
                        "anchor": True,
                    }
                )

        self._validate_invariants(extracted_recipes)
        return extracted_recipes

    def _validate_invariants(self, recipes: list[dict[str, Any]]) -> None:
        """
        Enforces canonical reversible-marker invariants.
        """
        rev_counts: dict[str, int] = {}
        optrev_orphans: set[str] = set()

        for recipe in recipes:
            # Check for markers in the recipe (Text, List, Table, Yaml all have different shapes now)
            markers = []
            if "props_info" in recipe:  # Text
                markers = recipe["props_info"]
            elif "marker" in recipe:  # List, Table, Yaml
                markers = [recipe["marker"]]

            for marker in markers:
                if marker.is_reversible:
                    rev_counts[marker.name] = rev_counts.get(marker.name, 0) + 1
                elif marker.is_optional:
                    optrev_orphans.add(marker.name)

        # Check for multiple revs
        for name, count in rev_counts.items():
            if count > 1:
                raise SLDBASTError(
                    f"Multiple canonical 'rev' markers found for field '{name}'."
                )
            if name in optrev_orphans:
                optrev_orphans.remove(name)

        # Check for orphans
        if optrev_orphans:
            orphan_list = ", ".join(sorted(optrev_orphans))
            raise SLDBASTError(
                f"Optional 'optrev' markers found for fields without a canonical 'rev' source: {orphan_list}"
            )
