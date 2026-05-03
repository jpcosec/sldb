import re
from typing import Any

from markdown_it.tree import SyntaxTreeNode

from sldb.core.node_handler import SharedNodeHandler


class TemplateExtractor:
    """
    Extracts deterministic search recipes from template block nodes.
    """

    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def extract_nodes(self, block_nodes: list[SyntaxTreeNode]) -> list[dict[str, Any]]:
        extracted_recipes = []

        for outer_index, block_node in enumerate(block_nodes):
            outer_type = getattr(block_node, "type", "")
            found_recipe_in_block = False

            def dive(node: SyntaxTreeNode, current_path: list[int]):
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
                                    "outer_tag": getattr(block_node, "tag", ""),
                                    "inner_path": current_path,
                                }
                            )
                            extracted_recipes.append(recipe)
                            found_recipe_in_block = True
                        return

                if handler_key == "text" or not getattr(node, "children", []):
                    literal_recipes = self.node_handler.handlers["text"].compile_recipe(
                        node
                    )
                    if literal_recipes:
                        for recipe in literal_recipes:
                            recipe.update(
                                {
                                    "outer_index": outer_index,
                                    "outer_type": outer_type,
                                    "outer_tag": getattr(block_node, "tag", ""),
                                    "inner_path": current_path,
                                }
                            )
                            extracted_recipes.append(recipe)
                            found_recipe_in_block = True

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
                        "outer_tag": getattr(block_node, "tag", ""),
                        "inner_path": [],
                        "props": [],
                        "regex": f"^{re.escape(content)}$" if content else "^$",
                        "handler": "text",
                        "anchor": True,
                    }
                )

        return extracted_recipes
